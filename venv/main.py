import sys
from sources.filter import *
from sources.Levenshtein import *
from sources.import_repository import *

def main():
    # Pull 2 repos from GitHub
    print("Pulling repositories")
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

