from git import Git


def clone_repo(clone_dir, repo_url):
    """
    Clones the specfied repository into the specified directory and
    returns the Repo class instance of the cloned repository.
    """
    return Git(clone_dir).clone(repo_url)

# This code will import the repos from git into the specified locations
# based on the args passed to the program
# it does not return anything


def import_repository(argv):
    if len(argv) == 3:
        cloned_directory_1 = argv[1]
        git_repo_1 = argv[2]
        print("You have chosen to compare a repo with itself... grabbing the directory...")
        clone_repo(cloned_directory_1, git_repo_1)
#       do more stuff here
    elif len(argv) == 5:
        cloned_directory_1 = argv[1]
        git_repo_1 = argv[2]
        cloned_directory_2 = argv[3]
        git_repo_2 = argv[4]
        print("You have chosen to compare two repos... grabbing the repos...")
        print("Grabbing the first repo...")
        clone_repo(cloned_directory_1, git_repo_1)
        print("Grabbing the second repo...")
        clone_repo(cloned_directory_2, git_repo_2)
#       do more stuff here
