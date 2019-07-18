from time import time

_last_time = time()


def time_snap(text=None):
    """
    Prints the time since the last call to this function in seconds.
    It is possible to supply a message to print along with the time.

    Arguments:
        text {str} (optional) -- Message to print with the time.
    """
    global _last_time
    current_time = time()
    print(current_time - _last_time, "seconds -", text)
    _last_time = current_time
