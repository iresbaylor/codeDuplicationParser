from bitarray import bitarray
from .pattern_clustering import clustering


def pattern_collection(tree_list_1, tree_list_2):
    """
    Compares two Abstract Syntax Trees representing two methods. The trees are
    provided as lists to provides indexes for the nodes within the tree
    """
    # Get the sizes of the trees
    size_tree_1 = len(tree_list_1)
    size_tree_2 = len(tree_list_2)

    # Checks whether a pairing has been compared. Set all to false (0) originally
    bit_string = '0' * len(tree_list_2)
    work_list = [bitarray(bit_string, endian='little') for _ in tree_list_1]

    # sets of minimum common subtrees (patterns) of trees
    pats = [[] for i in range(size_tree_1)]
    # sets of patterns which have been clustered together
    cpats = []

    # for all subtrees of both trees
    for i in range(size_tree_1):
        for j in range(size_tree_2):
            # if neither tree is a leaf node and the pair hasn't been checked
            if tree_list_1[i].children and tree_list_2[j].children and work_list[i][j]:
                # we have now checked this pairing
                work_list[i][j] = True
                # if the root nodes of the subtrees are equal
                if tree_list_1[i] == tree_list_2[j]:
                    # Add the results of anti-unify to the list of subtrees
                    pats[i].append(anti_unify(tree_list_1, tree_list_2, i, j, work_list))
    # for every set of patterns (one per node in the first tree)
    for pattern_set in pats:
        # run the clustering function on the pattern set
        cpats.append(clustering(pattern_set))
    # Return the sets of clustered patterns
    return cpats


def anti_unify(tree_list_1, tree_list_2, index_1, index_2, worklist):
    return [index_1, index_2]
