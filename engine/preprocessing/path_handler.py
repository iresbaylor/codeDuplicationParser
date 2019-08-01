from os.path import isdir
from .repoinfo import RepoInfo


def repo_path_to_local_path(repo_path):
    if isdir(repo_path):
        return repo_path

    info = RepoInfo.parse_repo_info(repo_path)

    if info and info.clone_or_pull():
        return info.dir
    else:
        return None
