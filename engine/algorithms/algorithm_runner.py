"""Module used for algorithm abstraction by providing a common interface."""

from .oxygen.oxygen import oxygen
from .chlorine.chlorine import chlorine_single_repo, chlorine_two_repos
from .iodine.iodine import iodine
from engine.errors.user_input import UserInputError
from . import OXYGEN, IODINE, CHLORINE


def run_single_repo(modules, algorithm):
    """
    Run the specified code clone detection algorithm on a single repository.

    Arguments:
        modules {list[list[TreeNode]]} -- List of the repo's modules.
        algorithm {string} -- Code clone detection algorithm to use.

    Raises:
        UserInputError -- If the algorithm name is invalid.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    if algorithm == OXYGEN:
        return oxygen(modules)
    elif algorithm == CHLORINE:
        return chlorine_single_repo(modules)
    elif algorithm == IODINE:
        raise UserInputError(f"\"{algorithm}\" can only be run with two repositories")
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")


def run_two_repos(modules1, modules2, algorithm):
    """
    Run the specified code clone detection algorithm on two repositores.

    Arguments:
        modules1 {list[list[TreeNode]]} -- List of first repo's modules.
        modules2 {list[list[TreeNode]]} -- List of second repo's modules.
        algorithm {string} -- Code clone detection algorithm to use.

    Raises:
        UserInputError -- If the algorithm name is invalid.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    if algorithm == CHLORINE:
        return chlorine_two_repos(modules1, modules2)
    elif algorithm == IODINE:
        return iodine(modules1, modules2)
    elif algorithm == OXYGEN:
        raise UserInputError(f"\"{algorithm}\" can only be run with one repository")
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")
