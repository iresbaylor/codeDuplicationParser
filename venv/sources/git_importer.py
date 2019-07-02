import git


# simple class to import from Git
class GitImporter:
    def clone_repo(self, clone_dir, git_link):
        git.Git(clone_dir).clone(git_link)