import re
from os import path, makedirs
from os.path import isdir, dirname
from git import Repo, InvalidGitRepositoryError, GitCommandError
from engine import __file__ as base_path
from ..errors.UserInputError import UserInputError
from urllib.parse import urlparse, urlunparse

# Base directory for all cloned repositories is "[main module root directory]/repos/".
clone_root_dir = path.join(dirname(base_path), "repos")


class RepoInfo:
    def __init__(self, url, server, user, name, local_dir, commit_hash=None):
        self.url = url
        self.server = server
        self.user = user
        self.name = name
        self.dir = local_dir
        self.hash = commit_hash

    def clone_or_pull(self):
        try:
            # If repo dir already exists, pull it.
            if isdir(self.dir):
                repo = Repo(self.dir)
                repo.remotes.origin.pull()

            # If the repo hasn't been cloned yet, clone it.
            else:
                repo = Repo.clone_from(self.url, self.dir)

            # Get HEAD's hash and store it in repo info.
            self.hash = repo.head.object.hexsha
            return True

        except InvalidGitRepositoryError:
            return False

        except GitCommandError:
            return False

    @staticmethod
    def parse_repo_info(repo_path):
        try:
            parts = urlparse(repo_path)
        except ValueError:
            return None

        if parts.username or parts.password or parts.query or parts.fragment \
                or parts.scheme not in {"https", "http", ""}:
            return None

        path_match = re.fullmatch(r"/*([\w\-\.]+)/*([\w\-\.]+)/*", parts.path)

        if not path_match:
            return None if parts.scheme else parse_repo_info("https://" + repo_path)

        repo_user = path_match[1]
        repo_name = path_match[2]

        scheme = parts.scheme or "https"
        server = parts.netloc or "github.com"

        # Inserting ":@" before hostname prevents username/password prompt
        full_url = urlunparse((scheme, ":@" + server,
                               f"/{repo_user}/{repo_name}", "", "", ""))

        clone_dir = path.join(clone_root_dir, server, repo_user, repo_name)

        return RepoInfo(full_url, server, repo_user, repo_name, clone_dir)
