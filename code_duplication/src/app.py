import os
import sys
from .common.repo_cloner import clone_repos
from .common.method_parser import get_modules_from_dir
from .common.args_checker import check_args
import ast


def main():
    # verifying inputs.
    # sys.argv should be in the following format:
    # sys.argv = {script name, git_1, git_2}
    flag = check_args(sys.argv)
    if not flag:
        print("    There was an error in your syntax. \n"
              "    Please verify that the git repos exist and your attempted directory to clone into are correct.")
        return

    from time import time

    start_time = time()
    # Close repositories and get their paths
    repos = clone_repos(sys.argv)
    clone_time = time()

    # ------- FOR TESTING PURPOSES ------------

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    print("Parsing methods in repositories...")
    modules, flat_nodes = get_modules_from_dir(repos[0])

    parse_time = time()

    # Tree-based type 1 check
    # method_count = len(methods)

    # for i1, m1 in enumerate(methods):
    #     for i2 in range(i1 + 1, method_count):
    #         if methods[i2] == m1:
    #             print("\n\n" + m1.dump())

    method1_time = time()

    type1_check(flat_nodes)

    method2_time = time()

    print(f"Clone: {clone_time - start_time} s\nParse: {parse_time - clone_time} s\nMethod 1: {method1_time - parse_time} s\nMethod 2: {method2_time - method1_time} s\nTotal: {method2_time - start_time} s")

    # -----------------------------------------


def type1_check(nodes):
    """
    Very simple type 1 code duplication check based on AST.dump() function.
    """

    WEIGHT_LIMIT = 20
    PRIORITY_CLASSES = [ast.Module, ast.ClassDef,
                        ast.FunctionDef, ast.AsyncFunctionDef]

    seen_nodes = set()

    for n in nodes:
        if n.weight < WEIGHT_LIMIT and not n.node.__class__ in PRIORITY_CLASSES:
            continue

        node_dump = n.dump()

        if node_dump in seen_nodes:
            print(f"{n}[{n.weight}]")
        else:
            seen_nodes.add(node_dump)
