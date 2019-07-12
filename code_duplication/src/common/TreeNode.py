import ast


class TreeNode:
    def __init__(self, node):
        self.node = node
        # TODO: This should be the actual value in case of childless nodes
        self.value = node.__class__.__name__

        self.all_nodes = list(ast.walk(self.node))
        self.child_nodes = [x for x in self.all_nodes if x is not self.node]

        grandchild_nodes = set()
        for child_node in self.child_nodes:
            grandchild_nodes.update(
                [x for x in ast.walk(child_node) if x is not child_node])

        self.direct_children = [
            TreeNode(x) for x in self.child_nodes if x not in grandchild_nodes]

        self.labels = set([
            x.id for x in self.all_nodes if isinstance(x, ast.Name)])

        # These values is set externally after all nodes are parsed
        self.index = None
        self.parent_index = None
        self.child_indices = []

    def dump(self):
        return ast.dump(self.node)

    def __str__(self):
        return f"{self.value}[{len(self.direct_children)} children; {len(self.labels)} labels; index={self.index}; parent={self.parent_index}; children={self.child_indices}]"

    def __repr__(self):
        return self.__str__()
