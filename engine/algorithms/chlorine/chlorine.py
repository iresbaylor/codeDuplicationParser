from collections import defaultdict
from ...utils.benchmark import time_snap
from ...utils.list_tools import flatten
from ...results.detected_clone import DetectedClone
from ...results.detection_result import DetectionResult

# Minimum weight of a single node used in comparison.
_MIN_NODE_WEIGHT = 50

# Minimum match / similarity coefficient required for two subtrees
# to be considered code clones and therefore returned.
_MIN_MATCH_COEFFICIENT = 0.8


def _get_skeleton(node_value, child_skeletons):
    return f"{node_value}[{', '.join(child_skeletons)}]" \
        if child_skeletons else node_value


def _get_skeleton_recursive(node):
    return _get_skeleton(node.value, [_get_skeleton_recursive(c) for c in node.children])


def _can_be_compared(node1, node2):
    """
    First get rid of nodes with a weight below the specified threshold.

    Checks if two nodes can be possible compared with each other.
    In order to be comparable, the nodes must have an equal value
    and they must have the exact same number of children.

    Arguments:
        node1 {TreeNode} -- First node.
        node2 {TreeNode} -- Second node.

    Returns:
        bool -- True if nodes can be compared, False if they cannot.

    """
    return \
        node1.weight >= _MIN_NODE_WEIGHT and \
        node2.weight >= _MIN_NODE_WEIGHT and \
        node1.value == node2.value and \
        len(node1.children) == len(node2.children)


def _type1_compare(node1, node2):
    """
    Compare two nodes and returns the weight of their matching subtrees
    and a skeleton string representing their common syntax tree skeleton.

    Arguments:
        node1 {TreeNode} -- First node.
        node2 {TreeNode} -- Second node.

    Returns:
        int -- Weight of the matching subtrees.
        string -- Common skeleton of the two nodes.

    """
    combined_weight = node1.weight + node2.weight

    if not _can_be_compared(node1, node2):
        # TODO: Maybe the weight of the hole should be omitted here.
        return 0, f"Hole({combined_weight})"

    skeleton = _get_skeleton_recursive(node1)
    if _get_skeleton_recursive(node2) == skeleton:
        return combined_weight, skeleton

    match_weight = 1
    child_skeletons = []

    for i, c in enumerate(node1.children):
        pair_weight, pair_skeleton = _type1_compare(c, node2.children[i])

        match_weight += pair_weight
        child_skeletons.append(pair_skeleton)

    return match_weight, _get_skeleton(node1.value, child_skeletons)


def _compare_internal(n1, n2, ignore_set, match_dict, skeleton_weight_dict):
    """
    Common logic shared by single-repo analysis and
    two repository comparison mode.

    Arguments:
        n1 {TreeNode} -- First node.
        n2 {TreeNode} -- Second node.
        ignore_set {set[TreeNode]} -- Set of nodes to ignore.
        match_dict {dict[string: set[TreeNode]]} -- Origin nodes of matches.
        skeleton_weight_dict {dict[string: int]} -- Skeleton weights.

    """
    if not _can_be_compared(n1, n2):
        return

    match_weight, match_skeleton = _type1_compare(n1, n2)

    if not match_weight:
        return

    if match_weight == max(n1.weight, n2.weight):
        ignore_set.update(n2.get_all_children())

    if match_weight / min(n1.weight, n2.weight) >= _MIN_MATCH_COEFFICIENT:
        match_dict[match_skeleton] |= {n1, n2}
        skeleton_weight_dict[match_skeleton] = match_weight


def _dict_to_result(match_dict, skeleton_weight_dict):
    """
    Compile the detection result together from the input dictionaries.

    Arguments:
        match_dict {dict[string: set[TreeNode]]} -- Origin nodes of matches.
        skeleton_weight_dict {dict[string: int]} -- Skeleton weights.

    """
    clones = []

    for k, v in match_dict.items():
        origin_list = list(v)
        clones.append(DetectedClone(
            origin_list[0].value, skeleton_weight_dict[k], origin_list))

    return DetectionResult(clones)


def chlorine_single_repo(modules):
    """
    Find all clones satisfying the settings at the top of this source file
    in a single repository given its modules.
    Detected code clones are printed on STDOUT, including the common skeleton,
    path to each clones (source file path, line number, column offset),
    size of each clone (number of nodes in its syntax tree) and their
    similarity percentage (number of matching nodes / total number of nodes).

    Arguments:
        modules {list[list[TreeNode]]} -- List of the repo's modules.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    time_snap("Function started")

    nodes = [m[0] for m in modules]

    time_snap("Module lists optimized")

    match_dict = defaultdict(set)
    skeleton_weight_dict = {}

    ignore_dict = {}
    start = 0

    while start < len(nodes):
        end = len(nodes)

        for i1 in range(start, end):
            n1 = nodes[i1]
            ignore_set = ignore_dict.pop(i1, set())

            for i2 in range(end):
                if i2 >= start and i2 <= i1:
                    continue

                n2 = nodes[i2]

                _compare_internal(n1, n2, ignore_set,
                                  match_dict, skeleton_weight_dict)

            for c in n1.children:
                index = len(nodes)
                nodes.append(c)

                if ignore_set:
                    ignore_dict[index] = ignore_set.copy()

        start = end

    time_snap("End of function")

    return _dict_to_result(match_dict, skeleton_weight_dict)


def chlorine_two_repos(modules1, modules2):
    """
    Find code clones between two repositories given their module lists.

    Clones must satisfy rules defined at the top of this source file.
    Detected clones are printed on STDOUT.
    See `find_clones_in_repo(repo_url)` for details on output format.

    Arguments:
        modules1 {list[list[TreeNode]]} -- List of first repo's modules.
        modules2 {list[list[TreeNode]]} -- List of second repo's modules.

    Returns:
        DetectionResult -- Result of the code clone detection.

    """
    time_snap("Function started")

    repo1_nodes = [m[0] for m in modules1]
    repo2_nodes = flatten(modules2)

    time_snap("Module lists optimized")

    match_dict = defaultdict(set)
    skeleton_weight_dict = {}

    ignore_dict = {}
    start = 0

    while start < len(repo1_nodes):
        end = len(repo1_nodes)

        for i1 in range(start, end):
            n1 = repo1_nodes[i1]
            ignore_set = ignore_dict.pop(i1, set())

            for n2 in repo2_nodes:
                if not _can_be_compared(n1, n2):
                    continue

                _compare_internal(n1, n2, ignore_set,
                                  match_dict, skeleton_weight_dict)

            first_index = len(repo1_nodes)
            repo1_nodes.extend(n1.children)

            if ignore_set:
                for i in range(first_index, len(repo1_nodes)):
                    ignore_dict[i] = ignore_set.copy()

        start = end

    time_snap("End of function")

    return _dict_to_result(match_dict, skeleton_weight_dict)
