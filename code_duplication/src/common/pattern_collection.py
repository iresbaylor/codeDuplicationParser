from bitarray import bitarray


def pattern_collection(tree_list_1, tree_list_2):
    """
    Compares two Abstract Syntax Trees representing two methods
    """
    # Get lengths
    len_tree_1 = len(tree_list_1)
    len_tree_2 = len(tree_list_2)

    # Checks whether a pairing has been compared
    bit_string = '1' * len(tree_list_2)
    work_list = [bitarray(bit_string, endian='little') for _ in tree_list_1]

    # minimum common subtrees (patterns) of trees
    pats = [[] for i in range(len_tree_1)]
    # clustered patterns
    cpats = []

    # for all subtrees that aren't leaf nodes
    for i in range(len_tree_1):
        for j in range(len_tree_2):
            # if work_list is true
            if work_list[i][j]:
                # set it to false
                work_list[i][j] = False
                # if the root nodes of the subtrees are equal
                if tree_list_1[i] == tree_list_2[j]:
                    # Add the results of anti-unify to the list of subtrees
                    pats[i].append(anti_unify(tree_list_1, tree_list_2, i, j, work_list))
    # for every node in the tree
    for pattern in pats:
        # Run the clustering function on the pats of each element
        cpats.append(clustering(pattern))
    # Return the values of the clustering function
    return cpats


def anti_unify(tree_list_1, tree_list_2, index_1, index_2, worklist):
    return [index_1, index_2]


def clustering(pattern):
    return pattern
