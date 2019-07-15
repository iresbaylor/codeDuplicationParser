import ast


class TreeNode:
    """
    Represents a single node of the Python code AST (Abstract Syntax Tree).
    Every node is also a tree of its own,
    with the exception of leaf (childless) nodes.
    """

    def __init__(self, node, origin_file):
        """
        Arguments:
            node -- Single raw node produced by the Python AST parser.
            origin_file {string} -- Relative path to the source file.
        """
        self.node = node
        self.origin = origin_file + (f" (L:{node.lineno} C:{node.col_offset})"
                                     if node._attributes else "")

        self.children = [TreeNode(n, origin_file)
                         for n in ast.iter_child_nodes(node)]

        self.weight = 1 + sum([c.weight for c in self.children])

        self.labels = [node.id] if isinstance(node, ast.Name) else []

        for c in self.children:
            self.labels.extend(c.labels)

        # Class name if the node has children, AST dump if it does not.
        self.value = node.id if isinstance(node, ast.Name) else \
            node.__class__.__name__ if self.children else self.dump()

        # These values are set externally after all nodes are parsed
        # during the node tree flattening process.
        self.index = None
        self.parent_index = None
        self.child_indices = []

    def dump(self):
        """
        Converts the node into a string using the built-in function.

        Returns:
            string -- String representation of the AST node.
        """
        return ast.dump(self.node)

    def __eq__(self, other):
        """
        Compares the node to another node recursively.
        This operator overload can be used for Type 1 clone detection.

        Arguments:
            other {TreeNode} -- Another tree node to compare this one to.

        Returns:
            bool -- True if the nodes are equivalent, False if they are not.
        """
        if not isinstance(other, TreeNode):
            return False
        elif other.dump() == self.dump():
            return True
        elif other.value != self.value:
            return False
        elif len(other.children) != len(self.children):
            return False

        for i, v in enumerate(other.children):
            if not v.__eq__(self.children[i]):
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.origin} - {self.value}"

    def __repr__(self):
        return self.__str__()
