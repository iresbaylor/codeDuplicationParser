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

    first_repo = request.args.get("first")

    return webpage.replace("#LOG#", "\n\n".join([f"{k[:20]} -- {v}" for k, v in type1_check_repo(first_repo, 30).items()]) if first_repo else "")

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
