from flask import Flask
from psycopg2 import connect, Error as PG_Error
from sys import stderr
from .credentials import conn_str
# from code_duplication import ???

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        conn = connect(conn_str)

        cur = conn.cursor()

        cur.execute("SELECT col FROM test;")
        return str(cur.fetchall())

    except PG_Error as ex:
        print("PostgreSQL Error:", ex, file=stderr)

    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    app.run()
