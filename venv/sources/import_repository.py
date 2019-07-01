from git_importer import GitImporter


def import_repository(argv):
    for i in argv:
        print(i)
    print()
    print()
    if len(argv) != 5 and len(argv) != 3:
        print("""\
Usage:
    python3 main.py [directory to be cloned to 1] [git repo 1] [directory to be cloned to 2] [git repo 2]
or (for comparing within a directory):
    python3 main.py [directory to be cloned to 1] [git repo 1]
        """)
        return
    elif len(argv) == 3:
        cloned_directory_1 = argv[1]
        git_repo_1 = argv[2]
        print("You have chosen to compare a repo with itself... grabbing the directory...")
        git_importer = GitImporter()
        git_importer.clone_repo(cloned_directory_1, git_repo_1)
#       do more stuff here
    elif len(argv) == 5:
        cloned_directory_1 = argv[1]
        git_repo_1 = argv[2]
        cloned_directory_2 = argv[3]
        git_repo_2 = argv[4]
        print("You have chosen to compare two repos... grabbing the repos...")
        git_importer = GitImporter()
        print("Grabbing the first repo...")
        git_importer.clone_repo(cloned_directory_1, git_repo_1)
        print("Grabbing the second repo...")
        git_importer.clone_repo(cloned_directory_2, git_repo_2)
#       do more stuff here
