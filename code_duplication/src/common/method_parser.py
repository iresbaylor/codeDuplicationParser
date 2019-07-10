import ast
from os import listdir, path
from os.path import isdir, isfile
from code_duplication.src.common.TreeNode import TreeNode


def _read_whole_file(file_path):
    """
    Read a text file into a single string.
    Assumes UTF-8 encoding.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def _read_ast_from_file(file_path):
    return ast.parse(_read_whole_file(file_path))


def _get_methods_from_file(file_path):
    file_ast = _read_ast_from_file(file_path)
    ast_nodes = ast.walk(file_ast)
    return [TreeNode(x) for x in ast_nodes if isinstance(x, ast.FunctionDef)]


def _recursive_listdir_py(directory):
    """
    Returns relative paths of all *.py files in the specified directory.
    If the provided argument is not a valid directory,
    an internal exception will be thrown by Python.
    That exception will most likely be NotImplementedError.
    """

    files = []

    for item in listdir(directory):
        fullpath = path.join(directory, item)

        if isfile(fullpath) and item.endswith('py'):
            files.append(fullpath)
        elif isdir(fullpath):
            files.extend(_recursive_listdir_py(fullpath))

    return files


def get_methods_from_dir(directory):
    """
    Find all *.py files in the directory recursively.
    Then finds all the methods in each file and
    stores them all in a list, which it then returns.
    """

    methods = []

    for file_path in _recursive_listdir_py(directory):
        methods.extend(_get_methods_from_file(file_path))

    return methods
