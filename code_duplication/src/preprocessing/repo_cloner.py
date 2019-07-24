from git import Git, Repo, InvalidGitRepositoryError
from os import path, makedirs
from os.path import isdir, dirname
from urllib.parse import urlparse
import re
from code_duplication import __file__ as base_path
from ..errors.UserInputError import UserInputError
from ..utils.config import config

# Base directory for all cloned repositories is "[main module root directory]/repos/".
clone_root_dir = path.join(dirname(base_path), "repos")


def _clone_repo(repo_url):
    """
    Clones the specified repository into a special internal directory and
    returns the directory path of the cloned repository.
    """

    # Make sure the base clone dir exists.
    makedirs(clone_root_dir, exist_ok=True)

    repo_name = re.sub(r"^.*?/([^/]+?)(?:\.git)?/?$",
                       r"\1", urlparse(repo_url).path)
    repo_dir = path.join(clone_root_dir, repo_name)

    try:
        # If repo dir already exists, pull
        if isdir(repo_dir):
            Repo(repo_dir).remotes.origin.pull()
        # Otherwise, clone the repo
        else:
            Git(clone_root_dir).clone(repo_url)

        return repo_dir

    # If anything goes wrong with the repo
    except InvalidGitRepositoryError:
        return None


def get_repo_dir(repo):
    """
    Attempts to process the given repository path in many different ways.
    If all of them fail, an error message will be printed and
    the script with exit with a non-zero exit code.
    If one of them succeeds, local path of the repository will be returned.

    Arguments:
        repo {string} -- Path to the repository or local directory.

    Returns:
        string -- Local path to the repository's directory.
    """

    # Local directory path
    if config.allow_local_access and isdir(repo):
        return repo

    # Name of a previously cloned repository
    repo_dir_by_name = path.join(clone_root_dir, repo)
    if re.fullmatch(r"^[\w\-]+$", repo) and isdir(repo_dir_by_name):
        return repo_dir_by_name

    # Shorthand for GitHub URLs: "[repository owner]/[repository name]"
    if re.fullmatch(r"^[\w\-]+/[\w\-]+(?:\.git)$", repo):
        repo_dir = _clone_repo("https://github.com/" + repo)
        if repo_dir:
            return repo_dir

    # NOTE: GitPython will pretend it has cloned a repository
    # even if no such repository existed. In reality,
    # it will just initialize a new local Git repository.
    repo_dir = _clone_repo(repo)
    if repo_dir:
        return repo_dir

    raise UserInputError(f"Invalid repository path: \"{repo}\"")
