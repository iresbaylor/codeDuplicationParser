from fastlog import log
from ..preprocessing.repo_cloner import get_repo_dir
from ..preprocessing.module_parser import get_modules_from_dir
from ..results.DetectedClone import DetectedClone
from ..results.DetectionResult import DetectionResult


def type1_check(modules, weight_limit=25):
    """
    Very simple type 1 code duplication check based on AST.dump() function.

    Arguments:
        modules (list[list[TreeNode]): Python ASTs from a repository
    """

    # PRIORITY_CLASSES = [ast.Module, ast.ClassDef,
    #                     ast.FunctionDef, ast.AsyncFunctionDef]

    node_dict = {}

    for m in modules:
        visited = set()

        for n in m:
            if n.parent_index in visited or n.weight < weight_limit:
                visited.add(n.index)
                continue

            node_dump = n.dump()

            if node_dump in node_dict:
                visited.add(n.index)
                node_dict[node_dump].append(n)
            else:
                node_dict[node_dump] = [n]

    return {k: v for k, v in node_dict.items() if len(v) > 1}


def type1_check_repo(repo, weight):
    repo_dir = get_repo_dir(repo)
    repo_modules = get_modules_from_dir(repo_dir)

    return DetectionResult([
        DetectedClone(node_list[0].value, 1, node_list) for node_list in
        type1_check(repo_modules, weight).values()])
