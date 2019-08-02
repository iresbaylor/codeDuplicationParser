class NodeOrigin:
    def __init__(self, file_path, line=None, col_offset=None, node_id=None):
        if file_path is None or \
            (node_id is None and (line is None or col_offset is None)) or \
                (node_id is not None and (line is not None or col_offset is not None)):

            raise ValueError(
                "File path and either ID or both line and column offset must be set to a non-None value")

        self.file = file_path
        self.line = line
        self.col_offset = col_offset
        self.id = node_id

    def __str__(self):
        return self.file + (f" (ID: {self.id:x})" if self.id else
                            f" (L: {self.line} C: {self.col_offset})")

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())
