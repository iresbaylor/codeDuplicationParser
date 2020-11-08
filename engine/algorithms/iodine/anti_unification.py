from ...nodes.pattern import PatternNode


def anti_unify(list1, list2, index1, index2, worktable, num_holes=0):
    """
    Create a tree of PatternNodes from two lists.

    Arguments:
        list1 {list of TreeNodes} -- first tree to be compared
        list2 {list of TreeNodes} -- second tree to be compared
        index1 {int} -- index of current TreeNode to be compared from list1
        index2 {int} -- index of current TreeNode to be compared from list2
        worktable {2D boolean array} -- keeps track of which two nodes have been checked together
        num_holes {int} -- number of holes accumulated in the tree
    """
    # mark the pair as checked/True
    worktable[index1].set(True, index2)
    # determine if subtrees are the same (and lengths same)
    if list1[index1] == list2[index2]:  # if true:
        # check if leaves
        if not list1[index1].child_indices and not list2[index2].child_indices:
            return PatternNode(list1[index1], list2[index2], list1[index1].value), num_holes
        elif len(list1[index1].child_indices) != len(list2[index2].child_indices):
            # verify child lists are same length; if not return hole
            # COME FIX AT SOME POINT
            num_holes += 1
            node1 = list1[index1]
            node2 = list2[index2]
            pat = PatternNode(node1, node2)
            return pat, num_holes
        else:  # if not leaves && same child index length:
            # iterate thru node's children, adding them as new children to the new fake node
            p = PatternNode(list1[index1], list2[index2], list1[index1].value)
            for cii, ci1 in enumerate(list1[index1].child_indices):
                ci2 = list2[index2].child_indices[cii]
                # call function on children to get their subtrees - RECURSION
                subtree, num_holes = anti_unify(list1, list2, ci1, ci2, worktable, num_holes)
                # associate with p
                p.add_child(subtree)
            return p, num_holes
    else:  # if false:
        return PatternNode(list1[index1], list2[index2]), num_holes
