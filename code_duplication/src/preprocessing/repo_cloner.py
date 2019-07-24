from git import Git, Repo, InvalidGitRepositoryError, GitCommandError
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

    Returns:
        string -- Cloned repository directory on success; None on failure.
    """

    # Make sure the base clone dir exists.
    makedirs(clone_root_dir, exist_ok=True)

    # NOTE: Only standard GitHub and GitLab are currently properly supported.
    match = re.fullmatch(
        r"^(?:https?://)?(?:[\w\-\.]*\.)?([\w\-]+)\.\w{1,10}/([\w\-]+)/([\w\-]+)(?:/?\.git)?/?$", repo_url)

    if not match:
        return None

    repo_dir = path.join(clone_root_dir, match[1], match[2], match[3])

    # If repo dir already exists, pull it.
    if isdir(repo_dir):
        try:
            Repo(repo_dir).remotes.origin.pull()
        except InvalidGitRepositoryError:
            return None

    # If the repo hasn't been cloned yet, clone it.
    else:
        # NOTE: Repo.clone_from() seems to return a Repo instance.
        # That might be useful for something later on.

        try:
            Repo.clone_from(repo_url, repo_dir)
        except GitCommandError:
            return None

    return repo_dir


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

    # TODO: This option should probably be removed in the future.
    # It is more confusing than it is practical now.

    # Path of a previously cloned repository: "[server]/[user]/[repo name]"
    repo_dir_by_name = path.join(clone_root_dir, repo)
    if re.fullmatch(r"^[\w\-]+/[\w\-]+/[\w\-]+$", repo) and isdir(repo_dir_by_name):
        return repo_dir_by_name

    # Shorthand for GitHub URLs: "[repository owner]/[repository name]"
    if re.fullmatch(r"^[\w\-]+/[\w\-]+(?:\.git)$", repo):
        repo_dir = _clone_repo("https://github.com/" + repo)

        if repo_dir:
            return repo_dir

    # Local directory path
    if isdir(repo):
        if config.allow_local_access:
            return repo
        else:
            raise UserInputError(
                f"Access to local directory denied: \"{repo}\"")

    # Full remote repository URL
    repo_dir = _clone_repo(repo)
    if repo_dir:
        return repo_dir

    raise UserInputError(f"Invalid repository path: \"{repo}\"")
