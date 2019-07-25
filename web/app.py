import os.path
from sys import stderr
from threading import Thread
from flask import Flask, request
from fastlog import log
from psycopg2 import connect, Error as PG_Error
from engine.preprocessing.module_parser import get_repo_modules_and_info
from engine.algorithms.algorithm_runner import run_single_repo, OXYGEN, CHLORINE, IODINE
from engine.utils.config import config
from engine.errors.UserInputError import UserInputError
from .credentials import conn_str

# Disable access to local file system
config.allow_local_access = False

app = Flask(__name__)


def _read_html(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name + ".html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

      
_INDEX_HTML = _read_html("index")
_MESSAGE_HTML = _read_html("message")
_RESULTS_HTML = _read_html("results")


def _analyze_repo(repo):
    try:
        conn = connect(conn_str)
        cur = conn.cursor()

        modules, repo_info = get_repo_modules_and_info(repo)

        if not modules or not repo_info:
            log.error("Unable to get the repository information")
            return

        cur.execute("""SELECT COUNT(*) FROM repos WHERE url = %s OR dir = %s OR ("server" = %s AND "user" = %s AND "name" = %s);""",
                    (repo_info.url, repo_info.dir, repo_info.server, repo_info.user, repo_info.name))

        count = cur.fetchone()[0]

        if count:
            return

        cur.execute("""INSERT INTO repos ("url", "dir", "server", "user", "name") VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                    (repo_info.url, repo_info.dir, repo_info.server, repo_info.user, repo_info.name))

        repo_id = cur.fetchone()[0]

        cur.execute(
            """INSERT INTO commits (repo_id, hash) VALUES (%s, %s) RETURNING id;""", (repo_id, repo_info.hash))

        commit_id = cur.fetchone()[0]

        conn.commit()

        result = run_single_repo(modules, OXYGEN)

        for c in result.clones:
            cur.execute("""INSERT INTO clusters (commit_id, "value", weight) VALUES (%s, %s, %s) RETURNING id;""",
                        (commit_id, c.value, c.match_weight))

            cluster_id = cur.fetchone()[0]

            for o, s in c.origins.items():
                cur.execute(
                    """INSERT INTO clones (cluster_id, origin, similarity) VALUES (%s, %s, %s);""", (cluster_id, o, s))

        cur.execute(
            """UPDATE commits SET finished = TRUE WHERE id = %s;""", (commit_id,))

        conn.commit()

    except PG_Error as ex:
        log.error("PostgreSQL: " + str(ex))

    finally:
        if conn:
            cur.close()
            conn.close()


def _get_repo_analysis(repo):  # TODO: Add docstring.
    try:
        conn = connect(conn_str)
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(
            """SELECT id FROM repos WHERE "url" = %s OR "name" = %s;""", (repo, repo))

        repos = cur.fetchall()

        if repos:
            repo_id = repos[0][0]

            cur.execute(
                """SELECT id FROM commits WHERE finished AND repo_id = %s;""", (repo_id,))

            commits = cur.fetchall()

            if commits:
                commit_id = commits[0][0]

                cur.execute(
                    """SELECT id, "value", weight FROM clusters WHERE commit_id = %s;""", (commit_id,))

                clusters = cur.fetchall()

                output = []

                for c in clusters:
                    cur.execute(
                        """SELECT origin, similarity FROM clones WHERE cluster_id = %s;""", (c[0],))

                    clones = cur.fetchall()

                    output.append((c, clones))

                return output

            else:
                return "Enqueued"

        else:
            thread = Thread(target=_analyze_repo, args=(repo,))
            thread.start()
            # _analyze_repo(repo)
            return "Added to queue"

    except PG_Error as ex:
        log.error("PostgreSQL: " + str(ex))
        return None

    finally:
        if conn:
            cur.close()
            conn.close()


@app.route("/")
def hello():
    content = ""

    repo = request.args.get("repo")
    if repo:
        try:
            result = _get_repo_analysis(repo)

            if isinstance(result, str):
                content = _MESSAGE_HTML.replace("#MSG#", "Result: " + result)
            elif result:
                clones = "<ol>" + "".join([("<li>" + c[0][1] + f" - Weight: {c[0][2]}" + "<ul>" +
                                            "".join(["<li>" + o[0] + f" - Similarity: {o[1] * 100:g} %" + "</li>" for o in c[1]]) +
                                            "</ul></li>") for c in result]) + "</ol>"

                content = _RESULTS_HTML.replace("#CLONES#", clones)

            else:
                content = _MESSAGE_HTML.replace(
                    "#MSG#", "<h4>No code clones detected. Congratulations!</h4>")

        except UserInputError as ex:
            content = _MESSAGE_HTML.replace(
                "#MSG#", "User Input Error: " + ex.message)

    return _INDEX_HTML.replace("#CONTENT#", content)
