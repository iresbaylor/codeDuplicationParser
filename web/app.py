from flask import Flask, request
# from psycopg2 import connect, Error as PG_Error
from sys import stderr
# from .credentials import conn_str
from code_duplication.src.secondary_algorithm.fast_check import type1_check_repo
import os.path

_INDEX_HTML = os.path.join(os.path.dirname(__file__), "index.html")

app = Flask(__name__)


@app.route("/")
def hello():
    with open(_INDEX_HTML, "r", encoding="utf-8") as f:
        webpage = f.read()

    output = ""

    first_repo = request.args.get("first_repo")
    if first_repo:
        result = type1_check_repo(first_repo, 15)

        with open("result.json", "w", encoding="utf-8") as f:
            f.write(result.json())

        output = "<ol>" + "".join([("<li>" + f"{c.value} - Weight: {c.weight} - Similarity: {c.similarity * 100:g} %" + "<ul>" +
                                    "".join(["<li>" + o + "</li>" for o in c.origins]) +
                                    "</ul></li>") for c in result.clones]) + "</ol>"

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
