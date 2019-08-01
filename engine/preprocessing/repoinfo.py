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
