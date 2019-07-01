import sys
from venv.git_importer import GitImporter


def main():
    for i in sys.argv:
        print(i)
    print()
    print()
    if len(sys.argv) != 5 and len(sys.argv) != 3:
        print("""\
Usage:
    python3 main [git repo 1] [directory 1] [git repo 2] [directory 2]
or (for comparing within a directory):
    python3 main [git repo 1] [directory 1]
        """)
        return
    elif len(sys.argv) == 3:
        git_repo_1 = sys.argv[1]
        cloned_directory_1 = sys.argv[2]
        print("You have chosen to compare a repo with itself... grabbing the directory...")
        git_importer = GitImporter()
        git_importer.clone_repo(git_repo_1, cloned_directory_1)
#       do more stuff here
    elif len(sys.argv) == 5:
        git_repo_1 = sys.argv[1]
        cloned_directory_1 = sys.argv[2]
        git_repo_2 = sys.argv[3]
        cloned_directory_2 = sys.argv[4]
        print("You have chosen to compare two repos... grabbing the repos...")
        git_importer = GitImporter()
        git_importer.clone_repo(git_repo_1, cloned_directory_1)
        git_importer.clone_repo(git_repo_2, cloned_directory_2)
#       do more stuff here


if __name__ == "__main__":
    main()

