import sys
import os
from sources.filter import *
from sources.Levenshtein import *
from sources.import_repository import *
from code_duplication.src.common.filter import filter_tokens
from code_duplication.src.common.Levenshtein import lev_distance
from code_duplication.src.common.import_repository import import_repository
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
    flag = check_args(sys.argv)
    if not flag:
        print("There was an error in your syntax. \n"
              "Please verify that the git repos exist and your attempted directory to clone into are correct.")
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