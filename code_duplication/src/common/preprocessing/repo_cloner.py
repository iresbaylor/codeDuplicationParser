from git import Git, Repo
from os import path, makedirs
from os.path import isdir, dirname
from urllib.parse import urlparse
import re
from code_duplication import __file__ as base_path

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

    if isdir(repo_dir):
        # TODO: Add try-except for InvalidGitRepositoryError
        # in case of empty directory, missing .git, etc.
        Repo(repo_dir).remotes.origin.pull()
    else:
        Git(clone_root_dir).clone(repo_url)

    return repo_dir

# This code will import the repos from git into the specified locations
# based on the args passed to the program
# it does not return anything


def clone_repos(argv):
    """
    Clones one or two repositories based on the command line arguments
    and then returns either either single repository path or a tuple
    containing the paths of both cloned repositories.

    Arguments:
        argv {list[string]} -- Command line arguments supplied to the app.
    """

    if len(argv) == 2:
        git_repo_1 = argv[1]
        print("Cloning the repository...")
        return _clone_repo(git_repo_1)

    elif len(argv) == 3:
        git_repo_1 = argv[1]
        git_repo_2 = argv[2]

        print("Cloning the first repository...")
        repo1 = _clone_repo(git_repo_1)

        print("Cloning the second repository...")
        repo2 = _clone_repo(git_repo_2)

        return (repo1, repo2)
