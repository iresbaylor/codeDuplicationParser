import collections
from sources.filter import *
from sources.Levenshtein import *

def main():
    # Pull 2 repos from GitHub
    print("Pulling repositories")
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

    print("Results:")


if __name__ == "__main__":
    main()

