from .oxygen.oxygen import oxygen
from .chlorine.chlorine import chlorine_single_repo, chlorine_two_repos
from ..errors.UserInputError import UserInputError


def run_single_repo(modules, algorithm):
    if algorithm == "oxygen":
        return oxygen(modules)
    elif algorithm == "chlorine":
        return chlorine_single_repo(modules)
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")
