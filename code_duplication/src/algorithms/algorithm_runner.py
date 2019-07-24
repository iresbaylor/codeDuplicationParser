from .oxygen.oxygen import oxygen
from ..errors.UserInputError import UserInputError


def run_single_repo(modules, algorithm):
    if algorithm == "oxygen":
        return oxygen(modules)
    else:
        raise UserInputError(f"Invalid algorithm name: \"{algorithm}\"")
