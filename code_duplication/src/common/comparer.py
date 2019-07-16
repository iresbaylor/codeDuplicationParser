from .Nodes.TreeNode import TreeNode
from .repo_cloner import _clone_repo
from .module_parser import get_modules_from_dir


def _get_skeleton(node, child_skeletons):
    return f"{node.value}[{', '.join(child_skeletons)}]" if child_skeletons \
        else node.value


def _get_skeleton_recursive(node):
    return _get_skeleton(node, [_get_skeleton_recursive(c) for c in node.children])


def _type1_compare(node1, node2):
    if node1.value != node2.value or node1.weight != node2.weight:
        return 0, f"Hole({(node1.weight + node2.weight) / 2 :g})"

    if node1.dump() == node2.dump():
        return node1.weight, _get_skeleton_recursive(node1)

    match_weight = 1
    child_skeletons = []

    if len(node1.children) == len(node2.children):
        for i, c in enumerate(node1.children):
            pair_weight, pair_skeleton = _type1_compare(c, node2.children[i])

            match_weight += pair_weight
            child_skeletons.append(pair_skeleton)

    return match_weight, _get_skeleton(node1, child_skeletons)


# def _type1_check(modules):
#     """
#     Very simple type 1 code duplication check based on AST.dump() function.
#     """

#     WEIGHT_LIMIT = 25

#     node_dict = {}

#     for m in modules:
#         visited = set()

#         for n in m:
#             if n.parent_index in visited or n.weight < WEIGHT_LIMIT:
#                 visited.add(n.index)
#                 continue

#             node_dump = n.dump()

#             if node_dump in node_dict:
#                 visited.add(n.index)
#                 node_dict[node_dump].append(n)
#             else:
#                 node_dict[node_dump] = [n]

#     for v in node_dict.values():
#         if len(v) > 1:
#             print(v)


def find_clones_in_repo(repo_url):
    repo_dir = _clone_repo(repo_url)
    repo_modules = get_modules_from_dir(repo_dir)
    # _type1_check(repo_modules)

    nodes = []

    for m in repo_modules:
        nodes.extend(m)

    for i1, n1 in enumerate(nodes):
        for i2 in range(i1 + 1, len(nodes)):
            n2 = nodes[i2]

            if n1.weight != n2.weight or n1.weight < 30:
                continue

            total_weight = n1.weight
            match_weight, match_skeleton = _type1_compare(n1, n2)

            match_percentage = round(match_weight / total_weight * 100, 2)

            if match_percentage > 75:
                print(
                    f"\n{match_skeleton}\n\n{n1}\n{n2}\nSimilarity: {match_percentage} % ({match_weight} out of {total_weight} nodes)")
