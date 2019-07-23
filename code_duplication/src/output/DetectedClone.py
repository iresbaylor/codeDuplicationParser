class DetectedClone:
    def __init__(self, value, nodes):
        """
        Initializes a new detected clone
        given its values and origin nodes.

        Arguments:
            value {string} -- String representation common to all the nodes.
            nodes {list[TreeNode]} -- List of origin nodes.
        """

        self.value = value
        self.origins = [n.origin for n in nodes]
        self.weight = sum([n.weight for n in nodes])
