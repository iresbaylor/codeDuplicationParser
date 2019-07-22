def print_node_list(node_list):
    """
    Prints a list of TreeNodes for debugging

    Arguments:
        node_list (list[TreeNode]): a list of tree nodes
    """
    for node in node_list:
        if node.parent_index is None:
            print_node(node, "", 0, node_list)


def print_node(node, indent, level, node_list):
    """
    Prints a TreeNode for debugging

    Arguments:
        node (TreeNode): node to print
        indent (str): space to print before node
        level (int): depth of node within the tree (0 for root)
        node_list (list[TreeNode]): list of TreeNodes to reference children of TreeNode
    """
    print(indent, "(", level, ")", node)
    for index in node.child_indices:
        for node in node_list:
            if node.index == index:
                print_node(node, indent + "    ", level + 1, node_list)
