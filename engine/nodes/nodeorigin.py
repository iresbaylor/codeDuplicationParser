"""Module containing the `NodeOrigin` class used to store node origin info."""


class NodeOrigin:
    """
    Class representing the origin of an AST node.

    Attributes:
        file {string} -- Source file from which the node originates.
        start {int|None} -- starting line number at which the node was found.
        end {int|None} -- ending line number at which the node was found.

    """

    def __init__(self, file_path, start=None, end=None):
        """
        Initialize a new node origin instance.

        Arguments:
            file_path {string} -- Path to the node's source file.

        Keyword Arguments:
            start {int} -- Starting line number of node's origin. (default: {None})
            end {int} -- Ending line number of node's origin. (default: {None})

        Raises:
            ValueError -- When file path is None or when only one of the two
                          source position specifiers is not None.

        """
        if file_path is None:
            raise ValueError(
                "File path must always be set to a non-None value")

        if (start is None) != (end is None):
            raise ValueError(
                "Either both the start and end lines must be set or neither")

        self.file = file_path
        self.start = start
        self.end = end

    def __str__(self):
        """Convert the node origin into a human-readable string representation."""
        return self.file + (f" ({self.start}, {self.end})"
                            if self.start and self.end else "")

    def __repr__(self):
        """Return a string representation of the node origin."""
        return self.__str__()

    def __hash__(self):
        """
        Get hash of the node origin.

        The `id` of the node origin is used right now, so two equivalent
        node origins may not necessarily have the same hash.
        That would be a problem normally, but it works fine in this project.

        """
        return hash(id(self))
