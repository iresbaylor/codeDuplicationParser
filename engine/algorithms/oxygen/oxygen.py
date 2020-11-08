"""Module containing logic and interface of the Oxygen algorithm."""

from ...results.detected_clone import DetectedClone
from ...results.detection_result import DetectionResult
import os


# Minimum weight of a single node used in comparison.
_MIN_NODE_WEIGHT = int(os.environ.get("OXYGEN_MIN_NODE_WEIGHT", 20))


def _dump_node(node):
    """Dump node's value and all of its children recursively."""
    return f"{node.value}[{'; '.join([_dump_node(c) for c in node.children])}]"


def oxygen(modules):
    """
    Run basic type 1 code duplication check based on AST.dump() function.

    Arguments:
        modules (list[list[TreeNode]): Modules in locally standardized format.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    # Dictionary of all the different shapes of node trees.
    # Key is a string representation of the tree.
    # Value is a list of all nodes with the exact same string representation.
    # These nodes are often referred to as "origins" throughout the project.
    node_dict = {}

    for m in modules:
        # Set of visited nodes is used to prevent recursively comparing
        # children of known perfect matches to avoid redundant clones.
        visited = set()

        for n in m:
            if n.parent_index in visited or n.weight < _MIN_NODE_WEIGHT:
                visited.add(n.index)
                continue

            node_dump = _dump_node(n)

            if node_dump in node_dict:
                visited.add(n.index)
                node_dict[node_dump].append(n)
            else:
                node_dict[node_dump] = [n]

    # Transform the dictionary into a list of detected clones.
    clones = []

    for origin_list in node_dict.values():
        if len(origin_list) <= 1:
            continue

        clones.append(DetectedClone(
            origin_list[0].value, origin_list[0].weight, nodes=origin_list))

    return DetectionResult(clones)
