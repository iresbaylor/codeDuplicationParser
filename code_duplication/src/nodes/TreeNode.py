import ast

_IGNORE_CLASSES = [ast.Load, ast.Store, ast.Del,
                   ast.AugLoad, ast.AugStore, ast.Param]


class TreeNode:
    """
    Represents a single node of the Python code AST (Abstract Syntax Tree).
    Every node is also a tree of its own,
    with the exception of leaf (childless) nodes.

    Attributes:
        node {AST} -- Original AST node generated by Python's built-in parser.
        origin {string} -- Origin of the node (file path, line and column).
        children {list[TreeNode]} -- List of direct children of this node.
        weight {int} -- Total number of nodes in this node's tree.
        names {list[string]} -- All names / symbols used in this node's tree.
        value {string} -- String representation of just this node.
        index {int} -- Index of this node (in an external flat list of nodes).
        parent_index {int} -- Index of parent node. None if this is root node.
        child_indices {list[int]} -- Indices of this node's direct children.
    """

    def __init__(self, node, origin_file):
        """
        Arguments:
            node -- Single raw node produced by the Python AST parser.
            origin_file {string} -- Relative path to the source file.
        """
        self.node = node
        self.origin = origin_file + (f" (L:{node.lineno} C:{node.col_offset})"
                                     if node._attributes else f" (ID:{id(node):x})")

        # Check if this type of node can have docstring.
        can_have_docstring = node.__class__ in [ast.ClassDef, ast.FunctionDef]

        # HACK: Ignore useless context-related children.
        # This should greatly reduce the total number of nodes.
        self.children = [TreeNode(n, origin_file) for n in
                         ast.iter_child_nodes(node)
                         if n.__class__ not in _IGNORE_CLASSES and
                         # Ignore docstrings in class and function definitions.
                         (not can_have_docstring or
                          not isinstance(n, ast.Expr) or
                          not isinstance(n.value, ast.Str))]

        self.weight = 1 + sum([c.weight for c in self.children])

        # Name nodes are handled in a special way.
        if isinstance(node, ast.Name):
            self.value = f"Name('{node.id}')"
            self.names = [node.id]

        else:
            # Class name if the node has children, AST dump if it does not.
            self.value = node.__class__.__name__ if self.children else self.dump()

            self.names = []
            for c in self.children:
                self.names.extend(c.names)

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
        return f"{self.origin} - {self.value} (W={self.weight})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.origin)