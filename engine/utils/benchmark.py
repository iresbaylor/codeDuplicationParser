"""Module containing helper functions used for benchmarking."""

from time import time
from fastlog import log

_last_time = time()


def time_snap(text=None):
    """
    Print the time since the last call to this function in seconds.

    It is possible to supply a message to print along with the time.

    Arguments:
        text {str} (optional) -- Message to print with the time.

    """
    global _last_time
    current_time = time()
    # TODO: This should probably be log.debug() instead.
    log.info(f"{current_time - _last_time} seconds - {text}")
    _last_time = current_time
