from ...src.primary_algorithm.pattern_clustering import clustering


class TestClustering(object):
    def test_one(self):
        assert clustering([]) == []
