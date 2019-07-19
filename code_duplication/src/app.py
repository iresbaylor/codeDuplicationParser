import sys
from .common.preprocessing.repo_cloner import clone_repos
from .common.preprocessing.module_parser import get_modules_from_dir
from .common.preprocessing.args_checker import check_args
from .common.primary_algorithm.pattern_collection import pattern_collection
from .common.utils.benchmark import time_snap
from .common.secondary_algorithm.fast_check import type1_check
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

    time_snap("Beginning analysis")
    # Close repositories and get their paths
    repos = clone_repos(sys.argv)
    time_snap("Cloned repositories")

    # ------- FOR TESTING PURPOSES ------------

    # Find all functions and parse their syntax tree using the TreeNode wrapper
    log.info("Parsing methods in repositories...")
    module_list_1 = get_modules_from_dir(repos[0])
    time_snap("Parsed first repository")

    module_list_2 = get_modules_from_dir(repos[1])
    time_snap("Parsed second repository")

    log.info("Beginning fast analysis...")
    type1_check(module_list_1)
    time_snap("Type 1 check for first repository")

    type1_check(module_list_2)
    time_snap("Type 1 check for second repository")

    log.info("Beginning full analysis...")
    clusters = []
    for module_tree_1 in module_list_1:
        for module_tree_2 in module_list_2:
            clusters.append(pattern_collection(module_tree_1, module_tree_2))

    time_snap("Analysis completed")

    for cluster_list in clusters:
        for pattern in cluster_list:
            if pattern:
                log.info("Possible clones:")
                log.info(pattern)
