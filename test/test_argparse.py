"""Module contaning tests for the CLI argument parsing logic."""

from pytest import raises
from argparse import Namespace
from cli.args_handler import parser
from engine.algorithms import IODINE, CHLORINE, OXYGEN
from . import test_repo1_url, test_repo2_url


def test_no_args():
    """Check if supplying no arguments throws an exceptions."""
    with raises(SystemExit) as ex:
        parser.parse_args([])
        assert ex.code != 0


def test_help_short():
    """Check if `-h` immediately exits successfully."""
    with raises(SystemExit) as ex:
        parser.parse_args(["-h"])
        assert ex.code == 0


def test_help_long():
    """Check if `--help` immediately exits successfully."""
    with raises(SystemExit) as ex:
        parser.parse_args(["--help"])
        assert ex.code == 0


def test_help_single():
    """Check if single-repository mode arguments are parsed correctly."""
    args = parser.parse_args([test_repo1_url])

    assert args is not None
    assert isinstance(args, Namespace)
    assert vars(args) == {"algorithm": IODINE,
                          "first_repo": test_repo1_url,
                          "second_repo": None}


def test_help_two():
    """Check if two-repository mode arguments are parsed correctly."""
    args = parser.parse_args([test_repo1_url, test_repo2_url])

    assert args is not None
    assert isinstance(args, Namespace)
    assert vars(args) == {"algorithm": IODINE,
                          "first_repo": test_repo1_url,
                          "second_repo": test_repo2_url}


def test_help_algorithm_oxygen():
    """Check if Oxygen algorithm arguments are parsed correctly."""
    args = parser.parse_args(
        ["--algorithm", OXYGEN, test_repo1_url])

    assert args is not None
    assert isinstance(args, Namespace)
    assert vars(args) == {"algorithm": OXYGEN,
                          "first_repo": test_repo1_url,
                          "second_repo": None}


def test_help_algorithm_chlorine():
    """Check if Chlorine algorithm arguments are parsed correctly."""
    args = parser.parse_args(
        ["--algorithm", CHLORINE, test_repo1_url, test_repo2_url])

    assert args is not None
    assert isinstance(args, Namespace)
    assert vars(args) == {"algorithm": CHLORINE,
                          "first_repo": test_repo1_url,
                          "second_repo": test_repo2_url}
