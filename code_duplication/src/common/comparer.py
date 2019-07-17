from .repo_cloner import _clone_repo
from .module_parser import get_modules_from_dir

_MIN_WEIGHT = 80
_MIN_MATCH_PERCENTAGE = 80


def _get_skeleton(node_value, child_skeletons):
    return f"{node_value}[{', '.join(child_skeletons)}]" \
        if child_skeletons else node_value


def _get_skeleton_recursive(node):
    return _get_skeleton(node.value, [_get_skeleton_recursive(c) for c in node.children])


def _can_be_compared(node1, node2):
    return node1.value == node2.value and len(node1.children) == len(node2.children)


def _type1_compare(node1, node2):
    combined_weight = node1.weight + node2.weight

    if not _can_be_compared(node1, node2):
        return 0, f"Hole({combined_weight})"

    skeleton = _get_skeleton_recursive(node1)
    if _get_skeleton_recursive(node2) == skeleton:
        return combined_weight, skeleton

    match_weight = 2
    child_skeletons = []

    for i, c in enumerate(node1.children):
        pair_weight, pair_skeleton = _type1_compare(c, node2.children[i])

        match_weight += pair_weight
        child_skeletons.append(pair_skeleton)

    return match_weight, _get_skeleton(node1.value, child_skeletons)


def find_clones_in_repo(repo_url):
    repo_dir = _clone_repo(repo_url)
    repo_modules = get_modules_from_dir(repo_dir)

    nodes = [m[0] for m in repo_modules]

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

                if n2 in ignore_set:
                    ignore_set.update(n2.children)
                    continue

                if not _can_be_compared(n1, n2):
                    continue

                total_weight = n1.weight + n2.weight
                if total_weight < 50:
                    continue

                match_weight, match_skeleton = _type1_compare(n1, n2)
                if not match_weight:
                    continue

                match_percentage = round(match_weight / total_weight * 100, 2)

                if match_percentage >= _MIN_MATCH_PERCENTAGE:
                    print(f"\n{match_skeleton}\n\n{n1}\n{n2}\n" +
                          f"Similarity: {match_percentage:g} % ({match_weight} out of {total_weight} nodes)")

                if match_weight == total_weight:
                    ignore_set.update(n2.children)

            for c in n1.children:
                index = len(nodes)
                nodes.append(c)

                if ignore_set:
                    ignore_dict[index] = ignore_set.copy()

        start = end
