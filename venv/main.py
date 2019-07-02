import sys
from sources.filter import *
from sources.Levenshtein import *
from sources.import_repository import *


def check_args(argv):
    if len(argv) != 5 and len(argv) != 3:
        print("""\
    Usage:
        python3 main.py [directory to be cloned to 1] [git repo 1] [directory to be cloned to 2] [git repo 2]
    or (for comparing within a directory):
        python3 main.py [directory to be cloned to 1] [git repo 1]
            """)
        return False
    return True


def main():
    flag = check_args(sys.argv)
    if not flag:
        return
    import_repository(sys.argv)

    # Tokenize repos
    print("Tokenizing repositories")
    list1 = {}
    list2 = {}
    # Filter out variable names - only control structures
    print("Filtering repositories")
    filter_tokens(list1, list2)
    # Use Levenhstein to compare tokens to tokens
    print("Comparing repositories")
    lev_distance(list1, list2)


if __name__ == "__main__":
    main()

