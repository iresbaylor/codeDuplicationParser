import ast
import tokenize
import os
from pprint import pprint


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

