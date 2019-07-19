import sys
from .common.preprocessing.repo_cloner import clone_repos
from .common.preprocessing.module_parser import get_modules_from_dir
from .common.preprocessing.args_checker import check_args
from .common.primary_algorithm.pattern_collection import pattern_collection
import ast
from time import time
from fastlog import log


def main():
    """
    Entry point of the application.
    """

    # verifying inputs.
    # sys.argv should be in the following format:
    # sys.argv = {script name, git_1, git_2}
    if not check_args(sys.argv):
        return

    start_time = time()
    # Close repositories and get their paths
    repos = clone_repos(sys.argv)
    clone_time = time()

    # ------- FOR TESTING PURPOSES ------------

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    log.info("Parsing methods in repositories...")
    module_list_1 = get_modules_from_dir(repos[0])
    parse_time_1 = time()

    module_list_2 = get_modules_from_dir(repos[1])
    parse_time_2 = time()

    type1_check(module_list_1)
    type1_time_1 = time()

    type1_check(module_list_2)
    type1_time_2 = time()

    clusters = []
    for module_tree_1 in module_list_1:
        for module_tree_2 in module_list_2:
            clusters.append(pattern_collection(module_tree_1, module_tree_2))

    analyze_time = time()

    log.info(f"Clone: {clone_time - start_time} s")
    log.info(f"Parse (repo 1): {parse_time_1 - clone_time} s")
    log.info(f"Parse (repo 2): {parse_time_2 - parse_time_1} s")
    log.info(f"Type 1 (repo 1): {type1_time_1 - parse_time_2} s")
    log.info(f"Type 1 (repo 2): {type1_time_2 - type1_time_1} s")
    log.info(f"Analysis: {analyze_time - type1_time_2} s")
    log.info(f"Total: {analyze_time - start_time} s")

    # -----------------------------------------

    # TODO: Need code to analyze and/or print clusters here


def type1_check(modules):
    """
    Very simple type 1 code duplication check based on AST.dump() function.
    """

    WEIGHT_LIMIT = 25
    # PRIORITY_CLASSES = [ast.Module, ast.ClassDef,
    #                     ast.FunctionDef, ast.AsyncFunctionDef]

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

    for v in node_dict.values():
        if len(v) > 1:
            log.success(v)


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
