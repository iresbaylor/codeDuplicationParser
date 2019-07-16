from urllib.parse import urlparse
import re

_USAGE_TEXT = """\
Usage:
    python3 -m code_duplication [first git repository] [second git repository]
or (for comparing within a single repository):
    python3 -m code_duplication [git repository]"""


def _check_url(url):
    """
    Performs a basic check of the repository URL.
    Prints
    """

    pieces = urlparse(url)

    url_ok = pieces.scheme and pieces.netloc and pieces.path and \
        pieces.scheme in ["http", "https"] and \
        re.fullmatch(r"^[a-zA-Z0-9\.\-]+\.\w+$", pieces.netloc) and \
        re.fullmatch(r"^[\w\.\-/_]+$", pieces.path)

    if not url_ok:
        print(f"Error: Invalid repository URL - \"{url}\"\n" +
              "Expected repository URL format: \"https://github.com/user/repository\"")

    return url_ok

# The below function will check to verify that there are the correct number of args
# it returns a boolean signifying whether the correct args were passed
# it will exit the program if it the passed args are not correct


def check_args(argv):
    """
    Checks the command line arguments and decides
    if the script should continue running.
    If there is any problem, an error message will be printed.

    Arguments:
        argv -- List of command line arguments.

    Returns:
        bool -- Indicates if the script should continue running.
    """

    if len(argv) == 1 or (len(argv) == 2 and argv[1] in ['-h', '--help', '--usage']):
        print(_USAGE_TEXT)
        return False

    if len(argv) < 2 or len(argv) > 3:
        print(
            f"Error: Invalid number of command line arguments - {len(argv) - 1}")
        print(_USAGE_TEXT)
        return False

    return _check_url(argv[1]) and (len(argv) < 3 or _check_url(argv[2]))
