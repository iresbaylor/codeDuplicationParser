import ast


class TreeNode:
    def __init__(self, node):
        self.node = node

        self.all_nodes = list(ast.walk(self.node))
        self.child_nodes = [x for x in self.all_nodes if x is not self.node]

        grandchild_nodes = set()
        for child_node in self.child_nodes:
            grandchild_nodes.update(
                [x for x in ast.walk(child_node) if x is not child_node])

        self.direct_children = [
            TreeNode(x) for x in self.child_nodes if x not in grandchild_nodes]

        self.labels = [x.id for x in self.all_nodes if isinstance(x, ast.Name)]

        # Class name if the node has children, AST dump if it does not.
        self.value = node.__class__.__name__ if self.direct_children else self.dump()

        if isinstance(node, ast.FunctionDef) and node.name == "pattern_collection":
            print("asd")

        # These values are set externally after all nodes are parsed
        # during the node tree flattening process.
        self.index = None
        self.parent_index = None
        self.child_indices = []

    def dump(self):
        return ast.dump(self.node)

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False

        elif other.dump() == self.dump():
            return True

        elif other.value != self.value:
            return False

        elif len(other.direct_children) != len(self.direct_children):
            return False

        else:
            for i, v in enumerate(other.direct_children):
                if not v.__eq__(self.direct_children[i]):
                    return False

        return True


    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.value}[{len(self.direct_children)} children; {len(self.labels)} labels; index={self.index}; parent={self.parent_index}; children={self.child_indices}]"

    def __repr__(self):
        return self.__str__()
