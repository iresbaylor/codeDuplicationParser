class NodeOrigin:
    def __init__(self, file_path, line=None, col_offset=None):
        if file_path is None:
            raise ValueError(
                "File path must always be set to a non-None value")

        if line is None != col_offset is None:
            raise ValueError(
                "Either both line number and column offset must be set or neither")

        self.file = file_path
        self.line = line
        self.col_offset = col_offset

    def __str__(self):
        return self.file + (f" (L: {self.line} C: {self.col_offset})"
                            if self.line and self.col_offset else "")

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(id(self))
