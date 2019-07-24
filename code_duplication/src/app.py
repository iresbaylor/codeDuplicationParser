import sys
from .preprocessing.args_handler import handle_args
from .preprocessing.module_parser import get_modules_from_dir
from .algorithms.iodine.iodine import iodine
from .utils.benchmark import time_snap
from .secondary_algorithm.fast_check import type1_check
from fastlog import log
from .errors.UserInputError import UserInputError


def main():
    """
    Entry point of the application.
    """

    try:
        # Parse command line arguments
        repos = handle_args(sys.argv)

        time_snap("Cloned repositories")

        # ------- FOR TESTING PURPOSES ------------

        # Find all functions and parse their syntax tree using the TreeNode wrapper
        log.info("Parsing methods in repositories...")
        module_list_1 = get_modules_from_dir(repos[0])

        if not module_list_1:
            raise UserInputError(f"First repository is empty: \"{repos[0]}\"")

        time_snap("Parsed first repository")

        module_list_2 = get_modules_from_dir(repos[1])

        if not module_list_2:
            raise UserInputError(f"Second repository is empty: \"{repos[1]}\"")

        time_snap("Parsed second repository")

        log.info("Beginning fast analysis...")
        type1_check(module_list_1)
        time_snap("Type 1 check for first repository")

        type1_check(module_list_2)
        time_snap("Type 1 check for second repository")

        log.info("Beginning full analysis...")
        iodine(module_list_1, module_list_2)
        time_snap("Analysis completed")

    except UserInputError as ex:
        if ex.message:
            log.error(ex.message)

        sys.exit(ex.code)
