import ast
import tokenize
import os
from pprint import pprint
from code_duplication.src.common.TreeNode import TreeNode


def time_to_tokenize_the_directory(directory, list1):
    for f in os.listdir(directory):
        if f.find('.py') != -1:
            print('running on', directory + '/' + f)
            then_there_were_tokens(directory + '/' + f, list1)


def then_there_were_tokens(filename, list1):
    with open(filename, 'rb') as f:
        for five_tuple in tokenize.tokenize(f.readline):
            print("---------------------")
            print(five_tuple)
            # print(five_tuple.type, five_tuple.string, five_tuple.end)
            list1.append(five_tuple)
            # print(five_tuple.string)
            # print(five_tuple.start)
            # print(five_tuple.end)
            # print(five_tuple.line)


def i_am_groot(directory1):
    with open(directory1, "r") as source:
        tree = ast.parse(source.read())
        print(ast.dump(tree))


def print_node_value(value):
    print(value)


def visit(node, handle_node):
    handle_node(node)
    for child in node.children:
        visit(child, handle_node)


def get_ast_from_file(file1):
    with open(file1, "r") as source:
        return ast.parse(source.read())


def get_methods_from_tree(tree):
    return [TreeNode(x) for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]


def get_methods_from_file(file1):
    return get_methods_from_tree(get_ast_from_file(file1))


def get_methods_from_directory(directory):
    methods = []

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        methods.extend((
            get_methods_from_file if os.path.isfile(item_path) and item_path.endswith('.py') else
            get_methods_from_directory if os.path.isdir(item_path) else
            lambda _: [])(item_path))

    return methods
