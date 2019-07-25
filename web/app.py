import os.path
from sys import stderr
from flask import Flask, request
# from psycopg2 import connect, Error as PG_Error
from engine.preprocessing.module_parser import get_modules_from_repo
from engine.algorithms.algorithm_runner import run_single_repo
from engine.utils.config import config
from engine.errors.UserInputError import UserInputError
# from .credentials import conn_str

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


@app.route("/")
def hello():
    content = ""

    repo = request.args.get("repo")
    if repo:
        try:
            modules = get_modules_from_repo(repo)
            result = run_single_repo(modules, "oxygen")

            if result.clones:
                clones = "<ol>" + "".join([("<li>" + c.value + f" - Weight: {c.match_weight}" + "<ul>" +
                                            "".join(["<li>" + orig + f" - Similarity: {sim * 100:g} %" + "</li>" for orig, sim in c.origins.items()]) +
                                            "</ul></li>") for c in result.clones]) + "</ol>"

                content = _RESULTS_HTML.replace("#CLONES#", clones)

            else:
                content = _MESSAGE_HTML.replace(
                    "#MSG#", "<h4>No code clones detected. Congratulations!</h4>")

        except UserInputError as ex:
            content = _MESSAGE_HTML.replace("#MSG#", ex.message)

    return _INDEX_HTML.replace("#CONTENT#", content)

    # try:
    #     conn = connect(conn_str)

    #     cur = conn.cursor()

    #     cur.execute("SELECT col FROM test;")
    #     return str(cur.fetchall())

    # except PG_Error as ex:
    #     print("PostgreSQL Error:", ex, file=stderr)

    # finally:
    #     if conn:
    #         cur.close()
    #         conn.close()


if __name__ == "__main__":
    app.run()
