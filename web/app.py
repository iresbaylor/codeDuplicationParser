from flask import Flask, request
# from psycopg2 import connect, Error as PG_Error
from sys import stderr
# from .credentials import conn_str
from code_duplication.src.secondary_algorithm.fast_check import type1_check_repo
from code_duplication.src.utils.config import config
import os.path
from code_duplication.src.errors.UserInputError import UserInputError

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
            result = type1_check_repo(repo, 15)

            with open("result.json", "w", encoding="utf-8") as f:
                f.write(result.json())

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
