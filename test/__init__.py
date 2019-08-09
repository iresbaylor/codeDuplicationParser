"""Package containing tests for all parts of this application (engine, interfaces)."""

from os.path import dirname, join as path_join

_test_dir = dirname(__file__)
_test_repos_dir = path_join(_test_dir, "repos")

test_repo1_dir = path_join(_test_repos_dir, "CodeDuplicateTest1")
test_repo2_dir = path_join(_test_repos_dir, "CodeDuplicateTest2")
