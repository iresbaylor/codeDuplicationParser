"""Module containing the core of the web UI application."""

from os.path import dirname, join as path_join
from flask import Flask, request
from easy_postgres import Connection as pg_conn
from mako.template import Template
from engine.errors.user_input import UserInputError
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
    clones = None

    repo = request.args.get("repo")
    if repo:
        try:
            result = get_repo_analysis(repo)

            if isinstance(result, str):
                msg = result

            elif result:
                clones = "".join([(f"""<li class="collection-item"><ul class="collection with-header"><li class="collection-header"><h5>{c.value} - Weight: {c.weight}</h5></li>""" +
                                   "".join([f"""<li class="collection-header">{o[0]} - Similarity: {o[1] * 100:g} %</li>""" for o in c.origins]) +
                                   "</ul></li>") for c in result])

            else:
                msg = "No code clones detected. Congratulations!"

        except UserInputError as ex:
            msg = "User Input Error: " + ex.message

    return index_template.render(msg=msg, clones=clones)
