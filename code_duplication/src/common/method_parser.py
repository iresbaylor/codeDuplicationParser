import ast
from os import listdir, path
from os.path import isdir, isfile
from .TreeNode import TreeNode
from collections import deque


def _read_whole_file(file_path):
    """
    Read a text file into a single string.
    Assumes UTF-8 encoding.
    """
    with open(file_path, "r", encoding="utf-8") as f:
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

        if isfile(fullpath) and item.endswith("py"):
            files.append(fullpath)
        elif isdir(fullpath):
            files.extend(_recursive_listdir_py(fullpath))

    return files


def _flatten_node_tree(nodes):
    node_queue = deque(nodes)
    flat_nodes = []

    while node_queue:
        n = node_queue.popleft()

        # Set this node's self-index.
        n.index = len(flat_nodes)

        # Add this node's index to the list of
        # children of its parent if it has any.
        if n.parent_index is not None:
            flat_nodes[n.parent_index].child_indices.append(n.index)

        # Set this node's children's parent index to this node's index.
        for c in n.direct_children:
            c.parent_index = n.index

        # Add this node's children to the queue.
        node_queue.extend(n.direct_children)

        # Add this node to the list of alraedy visited nodes.
        flat_nodes.append(n)

    return flat_nodes


def get_methods_from_dir(directory):
    """
    Finds all *.py files in the directory recursively.
    Then finds all the methods in each file and
    stores them all in a list, which it then returns.
    """

    methods = []

    for file_path in _recursive_listdir_py(directory):
        methods.extend(_get_methods_from_file(file_path))

    return methods, _flatten_node_tree(methods)
