"""Module containing the core of the web UI application."""

from os.path import dirname, join as path_join
from flask import Flask, request
from easy_postgres import Connection as pg_conn
from mako.template import Template
from engine.errors.user_input import UserInputError
from engine.results.detection_result import DetectionResult
from .credentials import db_url
from .analyzer import get_repo_analysis

_index_path = path_join(dirname(__file__), "index.mako")
index_template = Template(filename=_index_path)

app = Flask(__name__)

# Clean up the repository table
with pg_conn(db_url) as conn:
    conn.run("""UPDATE repos SET status = (SELECT id FROM states WHERE name = 'err_analysis') WHERE status = (SELECT id FROM states WHERE name = 'queue');""")


@app.route("/")
def web_index():
    """Homepage of the web interface."""
    msg = None
    repos = None
    clones = None

    repo_path = request.args.get("repo")

    if repo_path:
        try:
            result = get_repo_analysis(repo_path)

            # Should not happen.
            if result is None:
                msg = "Analysis error"

            elif isinstance(result, str):
                msg = result

            elif isinstance(result, DetectionResult):
                clones = result.clones

                if clones == []:
                    msg = "No code clones detected. Congratulations!"

            elif isinstance(result, list):
                repos = result

            # Should not happen, but just to be sure...
            # This make sure that something is always presented to the user.
            if not msg and not repos and not clones:
                msg = "Unable to analyze the repository"

        except UserInputError as ex:
            msg = "User Input Error: " + ex.message

    return index_template.render(msg=msg, repos=repos, clones=clones)
