"""Module containing the Iodine algorithm's interface."""

from .pattern_collection import pattern_collection
from ...results.detected_clone import DetectedClone
from ...results.detection_result import DetectionResult


def iodine(module_list_1, module_list_2):
    """
    Find clones between the two modules by comparing all possible subtrees of
    their methods. Returns the results.

    Arguments:
        modules1 {list[list[TreeNode]]} -- List of first repo's modules.
        modules2 {list[list[TreeNode]]} -- List of second repo's modules.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    clusters = []
    for module_tree_1 in module_list_1:
        for module_tree_2 in module_list_2:
            clusters.append(pattern_collection(
                module_tree_1, module_tree_2))

    clones = []
    for cluster_list in clusters:
        for pattern in cluster_list:
            if pattern:
                clones.append(DetectedClone(
                    pattern[0].value, pattern[0].get_match_weight(), nodes=pattern[0].nodes))

    return DetectionResult(clones)
