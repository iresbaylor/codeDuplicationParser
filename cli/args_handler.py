from os.path import isdir
from engine.errors.UserInputError import UserInputError
from engine.preprocessing.repoinfo import RepoInfo


_USAGE_TEXT = """\
Usage:
    python3 -m code_duplication <first repository> <second repository> - Repository comparison mode
    python3 -m code_duplication <repository>                           - Single repository mode

Valid repository path formats:
    Short GitHub repository path                - username/repository
    Full remote repository path                 - https://github.com/username/repository
    Absolute or relative local directory path   - /home/user/directory"""


def repo_path_to_local_path(repo_path):
    if isdir(repo_path):
        return repo_path

    info = RepoInfo.parse_repo_info(repo_path)

    if info and info.clone_or_pull():
        return info.dir
    else:
        return None


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

    return tuple(repo_path_to_local_path(a) for a in argv[1:])
