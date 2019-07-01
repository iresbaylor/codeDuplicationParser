from sources.filter import *

def main():
    # Pull 2 repos from GitHub
    print("Pulling repositories")
    # Tokenize repos
    print("Tokenizing repositories")
    # Filter out variable names - only control structures
    print("Filtering repositories")
    filter_tokens({}, {})
    # Use Levenhstein to compare tokens to tokens
    print("Comparing repositories")

    print("Results:")


if __name__ == "__main__":
    main()

