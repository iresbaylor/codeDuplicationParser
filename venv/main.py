import sys
from sources.filter import *
from sources.Levenshtein import *
from sources.import_repository import *
from urllib.parse import urlparse
import string


# The below function will check to verify that there are the correct number of args
# it returns a boolean signifying whether the correct args were passed
# it will exit the program if it the passed args are not correct
def check_args(argv):
    if len(argv) != 5 and len(argv) != 3:
        print("""\
    Usage:
        python3 main.py [directory to be cloned to 1] [git repo 1] [directory to be cloned to 2] [git repo 2]
    or (for comparing within a directory):
        python3 main.py [directory to be cloned to 1] [git repo 1]
            """)
        return False
    # testing the github URLs below
    if len(argv) == 3:
        pieces = urlparse(argv[2])
        flag = all([pieces.scheme, pieces.netloc])
        if flag:
            flag = set(pieces.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if flag:
                flag = pieces.scheme in ['http', 'https']
        return flag
    else:
        pieces1 = urlparse(argv[2])
        flag1 = all([pieces1.scheme, pieces1.netloc])
        if flag1:
            flag1 = set(pieces1.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if flag1:
                flag1 = pieces1.scheme in ['http', 'https']
        pieces2 = urlparse(argv[4])
        flag2 = all([pieces2.scheme, pieces2.netloc])
        if flag2:
            flag2 = set(pieces2.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if flag2:
                flag2 = pieces2.scheme in ['http', 'https']
        return flag1 and flag2


def main():
    flag = check_args(sys.argv)
    if not flag:
        print("There was an error in your syntax. Please check your syntax and try again.")
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

