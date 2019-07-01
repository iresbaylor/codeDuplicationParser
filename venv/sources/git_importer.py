import git


class GitImporter:
    def clone_repo(self, clone_dir, git_link):
        git.Git(clone_dir).clone(git_link)
