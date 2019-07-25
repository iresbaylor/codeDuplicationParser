from .oxygen.oxygen import oxygen
from .chlorine.chlorine import chlorine_single_repo, chlorine_two_repos
from ..errors.UserInputError import UserInputError


def run_single_repo(modules, algorithm):
    """
    Runs the specified code clone detection algorithm on a single repository.

    Arguments:
        modules {list[list[TreeNode]]} -- List of the repo's modules.
        algorithm {string} -- Code clone detection algorithm to use.

    Raises:
        UserInputError -- If the algorithm name is invalid.

    Returns:
        DetectionResult -- Result of the code clone detection.
    """

    if algorithm == "oxygen":
        return oxygen(modules)
    elif algorithm == "chlorine":
        return chlorine_single_repo(modules)
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")


def run_two_repos(modules1, modules2, algorithm):
    """
    Runs the specified code clone detection algorithm on two repositores.

    Arguments:
        modules1 {list[list[TreeNode]]} -- List of first repo's modules.
        modules2 {list[list[TreeNode]]} -- List of second repo's modules.
        algorithm {string} -- Code clone detection algorithm to use.

    Raises:
        UserInputError -- If the algorithm name is invalid.

    Returns:
        DetectionResult -- Result of the code clone detection.
    """

    if algorithm == "chlorine":
        return chlorine_two_repos(modules1, modules2)
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")
