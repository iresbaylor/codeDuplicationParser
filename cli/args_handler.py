"""Module containing functions for handling command-line arguments supplied by the user."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os.path import isdir
from engine.errors.user_input import UserInputError
from engine.preprocessing.repoinfo import RepoInfo


_REPO_PATH_FORMATS = """\
Valid repository path formats:
  Short GitHub repository path              - username/repository
  Full remote repository path               - https://github.com/username/repository
  Absolute or relative local directory path - /home/user/directory"""

parser = ArgumentParser(prog="python3 -m cli",
                        description="Detect code clones in Python 3 projects.",
                        epilog=_REPO_PATH_FORMATS,
                        formatter_class=RawDescriptionHelpFormatter)

parser.add_argument("first_repo", metavar="first-repo", type=str,
                    help="Path to the first repository")

parser.add_argument("second_repo", metavar="second-repo", type=str, nargs="?",
                    help="Path to the second repository")


def repo_path_to_local_path(repo_path):
    """
    Convert a repository path into a local file system path.

    This repository path is extended (compared to the repository path
    used by RepoInfo) by adding support for existing local directories.

    The process typically includes checking for a local directory or
    parsing a full or short repository URL and then cloning the repository.

    Arguments:
        repo_path {string} -- Path of a remote repository or a local directory.

    Returns:
        string -- Path of a local directory equivalent to the one
                  specified by the repository path.
                  In case of local directories, the paths are equal.

    """
    if repo_path is None:
        return None

    if isdir(repo_path):
        return repo_path

    info = RepoInfo.parse_repo_info(repo_path)

    if info and info.clone_or_pull():
        return info.dir
    else:
        return None


def handle_cli_args():
    """
    Parse the command line arguments and handle them.

    If there is any problem, an error message will be printed
    and the script will exit with a non-zero exit code.
    If everything goes right, tuple of local repository paths will be returned.

    Returns:
        tuple[string] -- Tuple of local repository paths.

    """
    args = parser.parse_args()

    return tuple(repo_path_to_local_path(p) for p in
                 (args.first_repo, args.second_repo))
