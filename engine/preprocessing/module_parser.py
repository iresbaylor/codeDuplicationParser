"""Module containing code used for parsing of modules and nodes from Python code."""

import ast
from os import listdir, path
from os.path import isdir, isfile, relpath
from ..nodes.tree import TreeNode
from collections import deque


def _read_whole_file(file_path):
    """
    Read a text file into a single string.

    Assumes UTF-8 encoding.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _read_ast_from_file(file_path):
    """
    Parse a module AST from the specified file.

    Arguments:
        file_path {string} -- Path of file to parse the AST from.

    Returns:
        AST parsed from the specified file.

    """
    return ast.parse(_read_whole_file(file_path))


def _get_tree_node_from_file(file_path, repo_path):
    """
    Parse a TreeNode representing the module in the specified file.

    Arguments:
        file_path {string} -- Path of file to parse the TreeNode from.

    Returns:
        TreeNode -- TreeNode parsed from the specified file.

    """
    return TreeNode(_read_ast_from_file(file_path),
                    relpath(file_path, repo_path))


def _recursive_listdir_py(directory):
    """
    Return relative paths of all *.py files in the specified directory.

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


def _flatten_module_nodes(module):
    """
    Convert a module TreeNode into a flat list of nodes in the module's AST.

    Arguments:
        module {TreeNode} -- TreeNode representing a module root node.

    Returns:
        list[TreeNode] -- List of all the nodes in the module's AST.

    """
    module_nodes = []
    node_queue = deque([module])

    while node_queue:
        n = node_queue.popleft()

        # Set this node's self-index.
        n.index = len(module_nodes)

        # Add this node's index to the list of
        # children of its parent if it has any.
        if n.parent_index is not None:
            module_nodes[n.parent_index].child_indices.append(n.index)

        # Set this node's children's parent index to this node's index.
        for c in n.children:
            c.parent_index = n.index

        # Add this node's children to the queue.
        node_queue.extend(n.children)

        # Add this node to the list of already visited nodes.
        module_nodes.append(n)

    return module_nodes


def get_modules_from_dir(directory):
    """
    Find all *.py files in the specified directory recursively.

    Every file is parsed as a module and converted into an AST.
    The parsed ASTs are converted into lists of all nodes in the ASTs.
    A list of all these lists is then constructed a returned.

    Arguments:
        directory {string} -- Path of directory to search for Python files.

    Returns:
        list[list[TreeNode]] -- List of lists of nodes from parsed modules.

    """
    return [_flatten_module_nodes(_get_tree_node_from_file(f, directory))
            for f in _recursive_listdir_py(directory)]
