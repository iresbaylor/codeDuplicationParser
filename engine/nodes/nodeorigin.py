"""Module containing the `NodeOrigin` class used to store node origin info."""


class NodeOrigin:
    """
    Class representing the origin of an AST node.

    Attributes:
        file {string} -- Source file from which the node originates.
        line {int|None} -- Line number at which the node was found.
        col_offset {int|None} -- Column offset within the line.
                                 Number of characters on the same
                                 line before the node's token.

    """

    def __init__(self, file_path, line=None, col_offset=None):
        """
        Initialize a new node origin instance.

        Arguments:
            file_path {string} -- Path to the node's source file.

        Keyword Arguments:
            line {int} -- Line number of node's origin. (default: {None})
            col_offset {int} -- Column offset of node. (default: {None})

        Raises:
            ValueError -- When file path is None or when only one of the two
                          source position specifiers is not None.

        """
        if file_path is None:
            raise ValueError(
                "File path must always be set to a non-None value")

        if (line is None) != (col_offset is None):
            raise ValueError(
                "Either both line number and column offset must be set or neither")

        self.file = file_path
        self.line = line
        self.col_offset = col_offset

    def __str__(self):
        """Convert the node origin into a human-readable string representation."""
        return self.file + (f" (L: {self.line} C: {self.col_offset})"
                            if self.line and self.col_offset else "")

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
