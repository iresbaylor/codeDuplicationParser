from ..nodes.PatternNode import PatternNode


def anti_unify(list1, list2, index1, index2, worktable):
    """
    Creates a tree of PatternNodes from two lists

    Arguments:
        list1 {list of TreeNodes} -- first tree to be compared
        list2 {list of TreeNodes} -- second tree to be compared
        index1 {int} -- index of current TreeNode to be compared from list1
        index2 {int} -- index of current TreeNode to be compared from list2
        worktable {2D boolean array} -- keeps track of which two nodes have been checked together
    """

    # mark the pair as checked/True
    worktable[index1][index2] = True
    # determine if subtrees are the same (and lengths same)
    if list1 == list2:  # if true:
        # check if leaves
        if not list1[index1].child_indices and not list2[index2].child_indices:
            return PatternNode(list1[index1], list2[index2], list1[index1].value)
        else:  # if not leaves:
            # iterate thru node's children, adding them as new children to the new fake node
            p = PatternNode(list1[index1], list2[index2], list1[index1].value)
            for c in list1[index1].child_indices:
                # call function on children to get their subtrees - RECURSION
                subtree = anti_unify(list1, list2, c, c, worktable)
                # associate with p
                p.add_child(subtree)
            return p
    else:  # if false:
        return PatternNode(list1[index1], list2[index2])
