"""Module containing the `AnalysisError` exception class."""


class AnalysisError(Exception):
    """
    Exception representing an error during a repository analysis.

    Attributes:
        message {string} -- Message explaining what went wrong.

    """

    def __init__(self, message):
        """
        Initialize a analysis error instance.

        Arguments:
            message {string} -- Message explaining what went wrong.

        """
        super().__init__(message)

        self.message = message
