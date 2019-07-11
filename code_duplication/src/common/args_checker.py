from urllib.parse import urlparse
import string


def _check_url(url):
    pieces = urlparse(url)

    if not all([pieces.scheme, pieces.netloc]):
        return False
    elif not set(pieces.netloc) <= set(string.ascii_letters + string.digits + "-."):
        return False
    elif not pieces.scheme in ["http", "https"]:
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
