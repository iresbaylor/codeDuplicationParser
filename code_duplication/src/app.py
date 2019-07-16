import sys
from .common.repo_cloner import clone_repos
from .common.module_parser import get_modules_from_dir
from .common.args_checker import check_args
import ast


def main():
    # verifying inputs.
    # sys.argv should be in the following format:
    # sys.argv = {script name, git_1, git_2}
    if not check_args(sys.argv):
        return

    from time import time

    start_time = time()
    # Close repositories and get their paths
    repos = clone_repos(sys.argv)
    clone_time = time()

    # ------- FOR TESTING PURPOSES ------------

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    print("Parsing methods in repositories...")
    modules = get_modules_from_dir(repos[0])

    parse_time = time()

    type1_check(modules)

    type1_time = time()

    print(f"Clone: {clone_time - start_time} s\nParse: {parse_time - clone_time} s\nType 1: {type1_time - parse_time} s\nTotal: {type1_time - start_time} s")

    # -----------------------------------------


def type1_check(modules):
    """
    Very simple type 1 code duplication check based on AST.dump() function.
    """

    WEIGHT_LIMIT = 10
    PRIORITY_CLASSES = [ast.Module, ast.ClassDef,
                        ast.FunctionDef, ast.AsyncFunctionDef]

    from hashlib import md5

    node_dict = {}

    for m in modules:
        visited = set()

        for n in m:
            if n.parent_index in visited or n.weight < WEIGHT_LIMIT:
                visited.add(n.index)
                continue

            node_dump = n.dump()

            if node_dump in node_dict:
                visited.add(n.index)
                node_dict[node_dump].append(n)
            else:
                node_dict[node_dump] = [n]

    for k, v in node_dict.items():
        if len(v) > 1:
            print(k, "\n", v, "\n")


def print_node_list(node_list):
    for node in node_list:
        if node.parent_index is None:
            print_node(node, "", 0, node_list)


def print_node(node, indent, level, node_list):
    print(indent, "(", level, ")", node)
    for index in node.child_indices:
        for node in node_list:
            if node.index == index:
                print_node(node, indent + "----", level + 1, node_list)
