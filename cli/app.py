import sys
from engine.preprocessing.args_handler import handle_args
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.iodine.iodine import iodine
from engine.utils.benchmark import time_snap
from fastlog import log
from engine.errors.UserInputError import UserInputError


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

        log.info("Beginning full analysis...")
        iodine(module_list_1, module_list_2)
        time_snap("Analysis completed")

    except UserInputError as ex:
        if ex.message:
            log.error(ex.message)

        sys.exit(ex.code)
