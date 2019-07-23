class DetectedClone:
    """
    Represents a single detected code clone.

    Attributes:
        value {string} -- String representation common to all the nodes.
        similarity {float} -- Similarity coefficient in range from 0 to 1,
                              where 0 means completely different and
                              1 means the nodes are all exactly equal.
        weight {int} -- Total weight of all the origin nodes.
        origins {list[string]} -- Origins of all nodes involved in this clone.
    """

    def __init__(self, value, similarity, nodes):
        """
        Initializes a new detected clone
        given its values and origin nodes.

        Arguments:
            value {string} -- String representation common to all the nodes.
            similarity {float} -- Similarity coefficient in range from 0 to 1,
                                  where 0 means completely different and
                                  1 means the nodes are all exactly equal.
            nodes {list[TreeNode]} -- List of origin nodes.
        """

        self.value = value
        self.similarity = similarity
        self.weight = sum([n.weight for n in nodes])
        self.origins = [n.origin for n in nodes]

    def dict(self):
        """
        Returns a dictionary representation of the detected clone.
        This is necessary for later conversion to JSON, because
        there is no easy way to tell the JSON encoder how to encode
        instances of user-defined classes.

        Returns:
            dict -- Dictionary representation of the detected clone, including
                    all the attributes (value, similarity, weight, origins).
        """
        return self.__dict__
