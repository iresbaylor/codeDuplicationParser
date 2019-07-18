from .repo_cloner import _clone_repo
from .module_parser import get_modules_from_dir
from .benchmark import time_snap

_MIN_WEIGHT = 80
_MIN_MATCH_PERCENTAGE = 80


def _flatten(list_of_lists):
    flat = []

    for l in list_of_lists:
        flat.extend(l)

    return flat


def _get_all_children(node):
    children = node.children

    for c in children:
        children.extend(_get_all_children(c))

    return children


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
    time_snap("Start of function")
    repo_dir = _clone_repo(repo_url)
    time_snap("Repository cloned")
    repo_modules = get_modules_from_dir(repo_dir)

    nodes = [m[0] for m in repo_modules]
    time_snap("Modules / nodes parsed")

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
                if total_weight < _MIN_WEIGHT:
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

    time_snap("End of function")


def compare_two_repos(repo1_url, repo2_url):
    time_snap("Function start")
    repo1_dir = _clone_repo(repo1_url)
    time_snap("Clone first")
    repo2_dir = _clone_repo(repo2_url)
    time_snap("Clone second")
    repo1_modules = get_modules_from_dir(repo1_dir)
    time_snap("Get modules from first")
    repo2_modules = get_modules_from_dir(repo2_dir)
    time_snap("Get modules from second")
    repo1_nodes = [m[0] for m in repo1_modules]
    repo2_nodes = _flatten(repo2_modules)
    time_snap("Convert modules into nodes")

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

                total_weight = n1.weight + n2.weight
                if total_weight < _MIN_WEIGHT:
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

            first_index = len(repo1_nodes)
            repo1_nodes.extend(n1.children)

            if ignore_set:
                for i in range(first_index, len(repo1_nodes)):
                    ignore_dict[i] = ignore_set.copy()

        start = end

    time_snap("End of function")
