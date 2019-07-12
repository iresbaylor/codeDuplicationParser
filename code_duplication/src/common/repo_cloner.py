from git import Git, Repo
from os import path, makedirs
from os.path import isdir, dirname
from urllib.parse import urlparse
import re
from code_duplication import __file__ as base_path


def _clone_repo(repo_url):
    """
    Clones the specfied repository into a special internal directory and
    returns the directory path of the cloned repository.
    """

    # Base directory for all cloned repositories is "[main module root directory]/repos/".
    clone_dir = path.join(dirname(base_path), "repos")
    # Make sure the base clone dir exists.
    makedirs(clone_dir, exist_ok=True)

    repo_name = re.sub(r"^.*?/([^/]+?)(?:\.git)?/?$", r"\1", urlparse(repo_url).path)
    repo_dir = path.join(clone_dir, repo_name)

    if isdir(repo_dir):
        # TODO: Add try-except for InvalidGitRepositoryError
        # in case of empty directory, missing .git, etc.
        Repo(repo_dir).remotes.origin.pull()
    else:
        Git(clone_dir).clone(repo_url)

    return repo_dir

# This code will import the repos from git into the specified locations
# based on the args passed to the program
# it does not return anything


def clone_repos(argv):
    if len(argv) == 2:
        git_repo_1 = argv[1]
        print("You have chosen to compare a repo with itself... grabbing the directory...")
        return _clone_repo(git_repo_1)
#       do more stuff here
    elif len(argv) == 3:
        git_repo_1 = argv[1]
        git_repo_2 = argv[2]
        print("You have chosen to compare two repos... grabbing the repos...")
        print("Grabbing the first repo...")
        repo1 = _clone_repo(git_repo_1)
        print("Grabbing the second repo...")
        repo2 = _clone_repo(git_repo_2)
        return (repo1, repo2)
#       do more stuff here
