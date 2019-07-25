import os.path
from flask import Flask, request
# from psycopg2 import connect, Error as PG_Error
from engine.preprocessing.module_parser import get_modules_from_repo
from engine.algorithms.algorithm_runner import run_single_repo, OXYGEN, CHLORINE, IODINE
from engine.utils.config import config
from engine.errors.UserInputError import UserInputError
# from .credentials import conn_str

# Disable access to local file system
config.allow_local_access = False

_INDEX_HTML = os.path.join(os.path.dirname(__file__), "index.html")

app = Flask(__name__)


@app.route("/")
def hello():
    with open(_INDEX_HTML, "r", encoding="utf-8") as f:
        webpage = f.read()

    output = ""

    repo = request.args.get("repo")
    if repo:
        try:
            modules = get_modules_from_repo(repo)
            result = run_single_repo(modules, OXYGEN)

            output = "<ol>" + "".join([("<li>" + c.value + f" - Weight: {c.match_weight}" + "<ul>" +
                                        "".join(["<li>" + orig + f" - Similarity: {sim * 100:g} %" + "</li>" for orig, sim in c.origins.items()]) +
                                        "</ul></li>") for c in result.clones]) + "</ol>"

        except UserInputError as ex:
            output = ex.message

    return webpage.replace("#LOG#", output)

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
