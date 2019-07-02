from sources.Levenshtein import *


class TestLevenshtein(object):
    def test_one(self):
        dist = lev_distance("hi", "hl")
        assert dist == 1

    def test_two(self):
        dist = lev_distance("hello", "h1")
        assert dist == 4
