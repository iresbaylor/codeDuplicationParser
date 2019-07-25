class DetectedClone:
    """
    Represents a single detected code clone.

    Similarity coefficient is a floating-point number between 0 and 1,
    where 0 means the subtrees are completely different and 1 means
    the subtrees are exactly equal and contain no holes.

    Attributes:
        value {string} -- String representation common to all the nodes.
        match_weight {int} -- Weight of the matching subtree skeleton.
        origins {dict[string: float]} -- Origins and similarity coefficients.
                                         Origins are used for keys.
                                         Similarity coefficients are values.
    """

    def __init__(self, value, match_weight, nodes):
        """
        Initializes a new detected clone
        given its values and origin nodes.

        Arguments:
            value {string} -- String representation common to all the nodes.
            match_weight {int} -- Weight of the matching subtree skeleton.
            nodes {list[TreeNode]} -- List of origin nodes.
        """

        self.value = value
        self.match_weight = match_weight
        self.origins = {n.origin: match_weight / n.weight for n in nodes}

    def dict(self):
        """
        Converts the detected clone into its dictionary representation.
        This is necessary for later conversion to JSON, because
        there is no easy way to tell the JSON encoder how to encode
        instances of user-defined classes.

        Returns:
            dict -- Dictionary representation of the detected clone,
                    including all of its attributes.
        """

        return self.__dict__
