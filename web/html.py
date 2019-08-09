"""Module containing pre-loaded HTML code used in the web application."""

from os.path import dirname, join as path_join


def _read_html(html_name):
    html_path = path_join(dirname(__file__), html_name + ".html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


index = _read_html("index")
message = _read_html("message")
results = _read_html("results")
