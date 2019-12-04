"""Module containing the CLI's core logic."""

import sys
from datetime import datetime
from .args_handler import handle_cli_args
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.algorithm_runner import run_single_repo, run_two_repos
from engine.utils.benchmark import time_snap
from fastlog import log
from engine.errors.user_input import UserInputError


def main():
    """Entry point of the application."""
    try:
        # Parse command start arguments
        repos, algorithm = handle_cli_args()

        time_snap("Arguments handled; Repositories parsed")

        module_list_1 = get_modules_from_dir(repos[0])
        time_snap("First repository modules parsed")

        if not module_list_1:
            raise UserInputError(f"First repository is empty: \"{repos[0]}\"")

        if repos[1]:
            module_list_2 = get_modules_from_dir(repos[1])
            time_snap("Second repository modules parsed")

            if not module_list_2:
                raise UserInputError(
                    f"Second repository is empty: \"{repos[1]}\"")

            log.info("Running a two-repository analysis...")
            result = run_two_repos(module_list_1, module_list_2, algorithm)

        else:
            log.info("Running a single-repository analysis...")
            result = run_single_repo(module_list_1, algorithm)

        time_snap("Analysis completed")

        # Save detection result to a JSON file.

        repo_0 = repos[0][repos[0].rfind('/') + 1:]
        json_filename = "clones_" + algorithm + "_" + repo_0 + "_"
        if repos[1]:
            repo_1 = repos[1][repos[1].rfind('/') + 1:]
            json_filename += repo_1 + "_"
        json_filename += datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"

        with open(json_filename, "w") as f:
            f.write(result.json())

    except UserInputError as ex:
        if ex.message:
            log.error(ex.message)

        sys.exit(ex.code)
