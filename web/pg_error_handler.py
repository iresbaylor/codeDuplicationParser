"""Module containing logic for handling PostgreSQL exceptions."""

from traceback import format_exc
from fastlog import log


def postgres_err(ex):
    """Log a PostgreSQL error (exception) with stack strace."""
    log.error(f"PostgreSQL: {ex}\n{format_exc()}")


def handle_pg_error(ex, conn, repo_id):
    """Log error and give the repository the analysis error status in db."""
    postgres_err(ex)

    if conn and repo_id is not None:
        conn.run("""UPDATE repos SET status = (SELECT id FROM states WHERE name = 'err_analysis') WHERE id = %s;""",
                 repo_id)
