import sys
from code_duplication.src.common.filter import filter_tokens
from code_duplication.src.common.Levenshtein import lev_distance
from code_duplication.src.common.import_repository import import_repository
from code_duplication.src.common.time_to_tokenize import *
from urllib.parse import urlparse
from code_duplication.src.common.directory_parser import list_files
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
    # testing the github URLs and that the directories exist below
    if len(argv) == 3:
        pieces = urlparse(argv[2])
        url_flag = all([pieces.scheme, pieces.netloc])
        if url_flag:
            url_flag = set(pieces.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if url_flag:
                url_flag = pieces.scheme in ['http', 'https']
        dir_flag = os.path.isdir(argv[1])
        return url_flag and dir_flag
    else:
        pieces1 = urlparse(argv[2])
        url_flag1 = all([pieces1.scheme, pieces1.netloc])
        if url_flag1:
            url_flag1 = set(pieces1.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if url_flag1:
                url_flag1 = pieces1.scheme in ['http', 'https']
        pieces2 = urlparse(argv[4])
        url_flag2 = all([pieces2.scheme, pieces2.netloc])
        if url_flag2:
            url_flag2 = set(pieces2.netloc) <= set(string.ascii_letters + string.digits + '-.')
            if url_flag2:
                url_flag2 = pieces2.scheme in ['http', 'https']
        dir_flag1 = os.path.isdir(argv[1])
        dir_flag2 = os.path.isdir(argv[3])
        return url_flag1 and url_flag2 and dir_flag1 and dir_flag2


def main():
    # verifying inputs.
    # sys.argv should be in the following format:
    # sys.argv = {script name, dir_1, git_1, dir_2, git_2}
    flag = check_args(sys.argv)
    if not flag:
        print("    There was an error in your syntax. \n"
              "    Please verify that the git repos exist and your attempted directory to clone into are correct.")
        return
    import_repository(sys.argv)
    # Tokenize repos
    print("Tokenizing repositories")

    # ------- FOR TESTING PURPOSES ------------
    if len(sys.argv) >= 2:
        # Find all functions and parse their syntax tree using the TreeNode wrapper
        for method in get_methods_from_directory(sys.argv[1]):
            print(method)

        return
    # -----------------------------------------

    list1 = []
    list2 = []
    # if we can set the variables below to the directories we want to compare, it should work
    directory1 = sys.argv[1]
    directory2 = sys.argv[3]
    # time_to_tokenize_the_directory(directory1, list1)
    # time_to_tokenize_the_directory(directory2, list2)
    i_am_groot(directory1)
    # "./code_duplication/src/common/Levenshtein.py"
    i_am_groot(directory2)
    # Filter out variable names - only control structures
    print("Filtering repositories")
    filter_tokens(list1, list2)
    # Use Levenhstein to compare tokens to tokens
    print("Comparing repositories")
    lev_distance(list1, list2)
