import os
import sys
from .common.repo_cloner import clone_repos
from .common.method_parser import get_methods_from_dir
from .common.args_checker import check_args
from .common.pattern_collection import pattern_collection


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

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    print("Parsing methods in repositories...")
    _, node_list_1 = get_methods_from_dir(repos[0])
    _, node_list_2 = get_methods_from_dir(repos[1])

    clusters = []
    for module1 in node_list_1:
        for module2 in node_list_2:
            clusters.append(pattern_collection(module1, module2))

    print(clusters)

    # ------- FOR TESTING PURPOSES ------------

    # Dump all nodes' information into stdout.
    print_node_list(node_list_1)

    # -----------------------------------------


def print_node_list(node_list):
    for node in node_list:
        if node.parent_index is None:
            print_node(node, "", 0, node_list)


def print_node(node, indent, level, node_list):
    print(indent, "(", level, ")", node)
    for index in node.child_indices:
        for node in node_list:
            if node.index == index:
                print_node(node, indent + "    ", level + 1, node_list)
