from os.path import join as path_join
from unittest import TestCase
from pytest import mark
from . import test_data_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.algorithm_runner import run_two_repos, IODINE, CHLORINE
from engine.results.detection_result import DetectionResult


class SingleFuncDefTest(TestCase):
    def setUp(self):
        data_dir = path_join(test_data_dir, "single_func_def")

        reference_dir = path_join(data_dir, "reference")
        different_dir = path_join(data_dir, "different")
        type1_dir = path_join(data_dir, "type1")
        type2_dir = path_join(data_dir, "type2")

        self.reference = get_modules_from_dir(reference_dir)
        self.different = get_modules_from_dir(different_dir)
        self.type1 = get_modules_from_dir(type1_dir)
        self.type2 = get_modules_from_dir(type2_dir)

    def _single_func_def(self, second, algorithm):
        result = run_two_repos(self.reference, second, algorithm)

        assert result is not None
        assert isinstance(result, DetectionResult)

        return result

    # different/

    def _single_func_def_different(self, algorithm):
        result = self._single_func_def(self.different, algorithm)

        for c in result.clones:
            assert c.match_weight < 10

    def test_single_func_def_different_iodine(self):
        self._single_func_def_different(IODINE)

    def test_single_func_def_different_chlorine(self):
        self._single_func_def_different(CHLORINE)

    # type1/

    def _single_func_def_type1(self, algorithm):
        result = self._single_func_def(self.type1, algorithm)

        assert len(result.clones) > 0

    def test_single_func_def_type1_iodine(self):
        self._single_func_def_type1(IODINE)

    def test_single_func_def_type1_chlorine(self):
        self._single_func_def_type1(CHLORINE)
