import argparse

"""
https://docs.python.org/3.5/library/argparse.html
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Process RC & RC27 for batters')
    parser.add_argument('-y', '--year', type=int, required=True, help='year to process data for')
    parser.add_argument('-n', '--number', default=-1, type=int, help='Number of players to list (defaults to all)')
    parser.add_argument('-a', '--attribute', default='RC', help='Attribute to sort (defaults to RC)')
    parser.add_argument('-m', '--min', default=0, type=int, help='Minimum number of at-bats (defaults to 0)')

    return parser.parse_args()
