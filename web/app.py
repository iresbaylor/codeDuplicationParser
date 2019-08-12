"""Module containing the core of the web UI application."""

from flask import Flask, request
from easy_postgres import Connection as pg_conn
from engine.errors.user_input import UserInputError
from web import html
from .credentials import db_url
from .analyzer import get_repo_analysis

app = Flask(__name__)

# Clean up the repository table
with pg_conn(db_url) as conn:
    conn.run("""UPDATE repos SET status = (SELECT id FROM states WHERE name = 'err_analysis') WHERE status = (SELECT id FROM states WHERE name = 'queue');""")


@app.route("/")
def web_index():
    """Homepage of the web interface."""
    content = ""

    repo = request.args.get("repo")
    if repo:
        try:
            result = get_repo_analysis(repo)

            if isinstance(result, str):
                content = html.message.replace("#MSG#", result)
            elif result:
                clones = "<ol>" + "".join([(f"<li>{c.value} - Weight: {c.weight}<ul>" +
                                            "".join([f"<li>{o[0]} - Similarity: {o[1] * 100:g} %</li>" for o in c.origins]) +
                                            "</ul></li><br>") for c in result]) + "</ol>"

                content = html.results.replace("#CLONES#", clones)

            else:
                content = html.message.replace(
                    "#MSG#", "No code clones detected. Congratulations!")

        except UserInputError as ex:
            content = html.message.replace(
                "#MSG#", "User Input Error: " + ex.message)

    return html.index.replace("#CONTENT#", content)
