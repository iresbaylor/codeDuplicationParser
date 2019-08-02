"""Module containing the core of the web UI application."""

import os.path
from threading import Thread
from flask import Flask, request
from fastlog import log
from psycopg2 import Error as PG_Error
from easy_postgres import Connection as pg_conn
from engine.preprocessing.repoinfo import RepoInfo
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.algorithm_runner import run_single_repo, OXYGEN
from engine.errors.UserInputError import UserInputError
from .credentials import db_url

app = Flask(__name__)


def _read_html(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name + ".html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


_INDEX_HTML = _read_html("index")
_MESSAGE_HTML = _read_html("message")
_RESULTS_HTML = _read_html("results")


def _analyze_repo(repo_path):
    try:
        db = pg_conn(db_url)

        repo_info = RepoInfo.parse_repo_info(repo_path)

        if not repo_info.clone_or_pull():
            log.error("Unable to clone repository:", repo_path)
            return

        modules = get_modules_from_dir(repo_info.dir)

        if not modules or not repo_info:
            log.error("Unable to get the repository information")
            return

        count = db.one("""SELECT COUNT(*) FROM repos WHERE url = %s OR dir = %s OR ("server" = %s AND "user" = %s AND "name" = %s);""",
                       repo_info.url, repo_info.dir, repo_info.server, repo_info.user, repo_info.name)

        if count:
            log.warning("Repository already present in database:", repo_path)
            return

        repo_id = db.one("""INSERT INTO repos ("url", "dir", "server", "user", "name") VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                         repo_info.url, repo_info.dir, repo_info.server, repo_info.user, repo_info.name)

        commit_id = db.one("""INSERT INTO commits (repo_id, hash) VALUES (%s, %s) RETURNING id;""",
                           repo_id, repo_info.hash)

        result = run_single_repo(modules, OXYGEN)

        for c in result.clones:
            cluster_id = db.one("""INSERT INTO clusters (commit_id, "value", weight) VALUES (%s, %s, %s) RETURNING id;""",
                                commit_id, c.value, c.match_weight)

            for o, s in c.origins.items():
                db.one("""INSERT INTO clones (cluster_id, origin, similarity) VALUES (%s, %s, %s);""",
                       cluster_id, o, s)

        db.one("""UPDATE commits SET finished = TRUE WHERE id = %s;""",
               commit_id)

    except PG_Error as ex:
        log.error("PostgreSQL: " + str(ex))


def _get_repo_analysis(repo):  # TODO: Add docstring.
    try:
        db = pg_conn(db_url)

        repos = db.all("""SELECT id FROM repos WHERE "url" = %(repo)s OR "name" = %(repo)s;""",
                       repo=repo)

        if repos:
            repo_id = repos[0]

            commits = db.all("""SELECT id FROM commits WHERE finished AND repo_id = %s;""",
                             repo_id)

            if commits:
                commit_id = commits[0]

                clusters = db.all_dict("""SELECT id, "value", weight FROM clusters WHERE commit_id = %s;""",
                                       commit_id)

                output = []

                for c in clusters:
                    clones = db.all_dict("""SELECT origin, similarity FROM clones WHERE cluster_id = %s;""",
                                         c.id)

                    output.append((c, clones))

                return output

            else:
                return "Enqueued"

        else:
            thread = Thread(target=_analyze_repo, args=(repo,))
            thread.start()
            return "Added to queue"

    except PG_Error as ex:
        log.error("PostgreSQL: " + str(ex))
        return None


@app.route("/")
def web_index():
    content = ""

    repo = request.args.get("repo")
    if repo:
        try:
            result = _get_repo_analysis(repo)

            if isinstance(result, str):
                content = _MESSAGE_HTML.replace("#MSG#", "Result: " + result)
            elif result:
                clones = "<ol>" + "".join([("<li>" + c[0].value + f" - Weight: {c[0].weight}" + "<ul>" +
                                            "".join(["<li>" + o.origin + f" - Similarity: {o.similarity * 100:g} %" + "</li>" for o in c[1]]) +
                                            "</ul></li><br>") for c in result]) + "</ol>"

                content = _RESULTS_HTML.replace("#CLONES#", clones)

            else:
                content = _MESSAGE_HTML.replace(
                    "#MSG#", "<h4>No code clones detected. Congratulations!</h4>")

        except UserInputError as ex:
            content = _MESSAGE_HTML.replace(
                "#MSG#", "User Input Error: " + ex.message)

    return _INDEX_HTML.replace("#CONTENT#", content)
