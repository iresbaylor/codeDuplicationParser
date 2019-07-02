import sys
from code_duplication.src.common.filter import filter_tokens
from code_duplication.src.common.Levenshtein import lev_distance
from code_duplication.src.common.import_repository import import_repository


# The below function will check to verify that there are the correct number of args
# it returns a boolean signifying whether the correct args were passed
# it will exit the program if it the passed args are not correct
def check_args(argv):
    if len(argv) != 5 and len(argv) != 3:
        print("""\
    Usage:
        python3 __main__.py [directory to be cloned to 1] [git repo 1] [directory to be cloned to 2] [git repo 2]
    or (for comparing within a directory):
        python3 __main__.py [directory to be cloned to 1] [git repo 1]
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