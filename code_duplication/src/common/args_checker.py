from urllib.parse import urlparse
import re


def _check_url(url):
    pieces = urlparse(url)

    if not pieces.scheme or not pieces.netloc or not pieces.path:
        return False
    elif pieces.scheme not in ["http", "https"]:
        return False
    elif not re.fullmatch(r"^[a-zA-Z0-9\.\-]+\.\w+$", pieces.netloc):
        return False
    elif not re.fullmatch(r"^[\w\.\-/_]+$", pieces.path):
        return False
    else:
        return True

# The below function will check to verify that there are the correct number of args
# it returns a boolean signifying whether the correct args were passed
# it will exit the program if it the passed args are not correct


def check_args(argv):
    if len(argv) < 2 or len(argv) > 3:
        print("""\
Usage:
    python3 -m code_duplication [first git repository] [second git repository]
or (for comparing within a single repository):
    python3 -m code_duplication [git repository]""")
        return False

    # testing the github URLs and that the directories exist below
    url_flag = _check_url(argv[1])

    if len(argv) == 3:
        url_flag &= _check_url(argv[2])

    return url_flag
