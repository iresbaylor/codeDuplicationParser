from urllib.parse import urlparse
import re
from .repo_cloner import get_repo_dir
from ..errors.UserInputError import UserInputError

_USAGE_TEXT = """\
Usage:
    python3 -m code_duplication <first repository> <second repository> - Repository comparison mode
    python3 -m code_duplication <repository>                           - Single repository mode"""


def _check_url(url):
    """
    Performs a basic check of the repository URL.
    """

    pieces = urlparse(url)

    return pieces.scheme and pieces.netloc and pieces.path and \
        pieces.scheme in ["http", "https"] and \
        re.fullmatch(r"^[a-zA-Z0-9\.\-]+\.\w+$", pieces.netloc) and \
        re.fullmatch(r"^[\w\.\-/_]+$", pieces.path)


def handle_args(argv):
    """
    Checks the command line arguments and handles them.
    If there is any problem, an error message will be printed
    and the script will exit with a non-zero exit code.
    If everything goes right, tuple of local repository paths will be returned.

    Arguments:
        argv -- List of command line arguments.

    Returns:
        tuple[string] -- Tuple of local repository paths.
    """

    if len(argv) == 1 or (len(argv) == 2 and argv[1] in ['-h', '--help', '--usage']):
        # Special case where the usage text is printed using the built-in
        # print function instead of the logging library because
        # the app exits right after the message is displayed.
        print(_USAGE_TEXT)
        raise UserInputError(None, 0)

    if len(argv) < 2 or len(argv) > 3:
        raise UserInputError(
            f"Invalid number of command line arguments: {len(argv) - 1}")

    return tuple(get_repo_dir(a) for a in argv[1:])