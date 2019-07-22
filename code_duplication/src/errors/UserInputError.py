class UserInputError(BaseException):
    """
    Exception related to user input.

    Attributes:
        message {string} -- Error message to print.
        code {int} -- Exit code to use.
    """

    def __init__(self, message, code=1):
        self.message = message
        self.code = code
