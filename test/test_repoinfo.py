"""Module containing unit tests for the RepoInfo class."""

import re
from unittest import TestCase
from shutil import rmtree
from os.path import join as path_join, relpath, isdir, samefile
from engine.preprocessing.repoinfo import RepoInfo, clone_root_dir


def test_repoinfo_parse_valid():
    """Test RepoInfo parser's ability to parse valid repository paths."""
    VALID_PATHS = [
        "https://github.com/user/repo",
        "HTTPS://GITHUB.COM/user/repo",
        "https://www.github.com/user/repo",
        "https://gitlab.com/user/repo",
        "HTTPS://GITLAB.COM/user/repo",
        "https://www.gitlab.com/user/repo",
        "http://github.com/user/repo",
        "https://github.com/user_user-user.user/repo.repo-repo_repo",
        "github.com/user/repo",
        "user/repo",
        "user//repo",
        "/user/repo",
        "user/repo/",
        "/user/repo/",
        "////user/repo////",
        "////user////repo////",
        "user_user-user.user/repo.repo-repo_repo",
        "///user_user-user.user///repo.repo-repo_repo///"
    ]

    for p in VALID_PATHS:
        assert RepoInfo.parse_repo_info(p) is not None, \
            f"\"{p}\" is a valid repository path"


def test_repoinfo_parse_invalid():
    """Test RepoInfo parser's ability to detect invalid repository paths."""
    INVALID_PATHS = [
        "",
        "https://",
        "https//github.com/user/repo",
        "https/github.com/user/repo",
        "://github.com/user/repo",
        "//github.com/user/repo"
        "/github.com/user/repo"
        "https://github,com/user/repo",
        "https://github;com/user/repo",
        "https;//github.com/user/repo",
        "https:\\\\github.com\\user\\repo",
    ]

    for p in INVALID_PATHS:
        assert RepoInfo.parse_repo_info(p) is None, \
            f"\"{p}\" is not a valid repository path"


def test_repoinfo_parse_attrib():
    """Test RepoInfo's attributes after parsing a repository path."""
    info = RepoInfo.parse_repo_info("hTTpS://GiTHuB.CoM/username/repository")

    assert info is not None

    assert info.url == "https://:@github.com/username/repository"

    assert info.server == "github.com"
    assert info.user == "username"
    assert info.name == "repository"

    expected_dir = path_join("github.com", "username", "repository")
    assert relpath(info.dir, clone_root_dir) == expected_dir

    assert info.hash is None


class RepoInfoCloneTest(TestCase):
    """Test case related to RepoInfo's repository cloning functionality."""

    def __init__(self, case):
        """Prepare the clone directory and call the super constructor."""
        super().__init__(case)

        self.clone_dir = path_join(clone_root_dir, "github.com",
                                   "calebdehaan", "codeDuplicationParser")

    # Delete the clone target directory before and after the test.
    tearDown = setUp = lambda self: rmtree(self.clone_dir, ignore_errors=True)

    def test_repoinfo_clone(self):
        """Test the RepoInfo's ability to clone a repository."""
        info = RepoInfo.parse_repo_info(
            "https://github.com/calebdehaan/codeDuplicationParser")

        assert info is not None
        assert info.clone_or_pull()

        assert info.url == "https://:@github.com/calebdehaan/codeDuplicationParser"
        assert info.server == "github.com"
        assert info.user == "calebdehaan"
        assert info.name == "codeDuplicationParser"

        assert info.dir is not None
        assert samefile(info.dir, self.clone_dir)
        assert isdir(path_join(info.dir, ".git"))

        assert info.hash is not None
        assert re.fullmatch(r"[0-9a-f]{40}", info.hash)
