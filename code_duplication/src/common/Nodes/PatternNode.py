class PatternNode:
    """
    More abstract representation of multiple similar TreeNodes.

    Attributes:
        nodes {list[TreeNode]} -- List of TreeNodes with the same skeleton.
        value {string} -- Common string representation of all the nodes.
        children {list[PatternNode]} -- List of node's direct children.
    """

    def __init__(self, node1, node2, value=None):
        """
        Creates a new PatternNode from two nodes and their common value.

        Arguments:
            node1 {TreeNode} -- First TreeNode sharing common skeleton.
            node2 {TreeNode} -- Second TreeNode sharing common skeleton.
            value {string} -- String representation common for all the nodes.
                              None if the PatternNode represents a hole.
        """
        self.nodes = [node1, node2]
        self.value = value or "Hole"
        self.children = []

    def add_nodes(self, *nodes):
        """
        Appends the supplied nodes to this node's list of origin nodes.

        Arguments:
            *nodes {tuple[TreeNode]} -- Origin TreeNodes of this node.
        """
        self.nodes.extend(nodes)

    def add_children(self, *children):
        """
        Appends the supplied nodes to this node's list of child nodes.

        Arguments:
            *nodes {tuple[PatternNode]} -- Children of this node.
        """
        self.children.extend(children)

    def __eq__(self, other):
        if not isinstance(other, PatternNode) or other.value != self.value or \
                len(other.children) != len(self.children):
            return False

        for i, c in enumerate(other.children):
            if c != self.children[i]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)
