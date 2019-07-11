import os
import sys
from .common.repo_cloner import clone_repos
from .common.method_parser import get_methods_from_dir
from .common.args_checker import check_args


def main():
    # verifying inputs.
    # sys.argv should be in the following format:
    # sys.argv = {script name, git_1, git_2}
    flag = check_args(sys.argv)
    if not flag:
        print("    There was an error in your syntax. \n"
              "    Please verify that the git repos exist and your attempted directory to clone into are correct.")
        return

    # Close repositories and get their paths
    repos = clone_repos(sys.argv)

    # ------- FOR TESTING PURPOSES ------------

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    print("Parsing method in repositories...")
    for method in get_methods_from_dir(repos[0]):
        print(method)

    # -----------------------------------------
