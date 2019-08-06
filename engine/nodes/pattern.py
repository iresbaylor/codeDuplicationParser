"""Module containing the `PatternNode` class."""

_HOLE = "Hole"


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
        Create a new PatternNode from two nodes and their common value.

        Arguments:
            node1 {TreeNode} -- First TreeNode sharing common skeleton.
            node2 {TreeNode} -- Second TreeNode sharing common skeleton.
            value {string} -- String representation common for all the nodes.
                              None if the PatternNode represents a hole.

        """
        self.nodes = [node1, node2]
        self.value = value or _HOLE
        self.children = []

    def add_node(self, node):
        """
        Append the supplied nodes to this node's list of origin nodes.

        Arguments:
            node {TreeNode} -- Node to be added to the list of origin nodes.

        """
        self.nodes.append(node)

    def add_child(self, child):
        """
        Append the supplied nodes to this node's list of child nodes.

        Arguments:
            child {PatternNode} -- Node that is a child of this node.

        """
        self.children.append(child)

    def skeleton_equals(self, other):
        """
        Check if this node's skeleton is equal to another node's.

        Arguments:
            other {PatterNode} -- Another node to compare this one with.

        Returns:
            bool -- True if the nodes have an equal skeleton, False otherwise.

        """
        if not isinstance(other, PatternNode) or other.value != self.value or \
                len(other.children) != len(self.children):
            return False

        for i, c in enumerate(other.children):
            if c != self.children[i]:
                return False

        return True

    def get_match_weight(self):
        """
        Calculate the weight of the matching skeleton of all origin nodes.

        Returns:
            int -- Weight of the matching skeleton.

        """
        return 0 if self.value == _HOLE else \
            (1 + sum([c.get_match_weight() for c in self.children]))

    def __str__(self):
        """Convert the pattern node into a human-readable string."""
        # FIXME: This doesn't seem right.
        return f"{self.value}(', '.join{[n.origin for n in self.nodes]})"

    def __repr__(self):
        """Return string representation of the pattern node."""
        return self.__str__()
