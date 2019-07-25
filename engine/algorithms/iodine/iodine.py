from .pattern_collection import pattern_collection
from ...results.DetectedClone import DetectedClone
from ...results.DetectionResult import DetectionResult
from fastlog import log


def iodine(module_list_1, module_list_2):
    clusters = []
    for module_tree_1 in module_list_1:
        for module_tree_2 in module_list_2:
            clusters.append(pattern_collection(
                module_tree_1, module_tree_2))

    clones = []
    for cluster_list in clusters:
        for pattern in cluster_list:
            if pattern:
                log(pattern)

    return clusters
