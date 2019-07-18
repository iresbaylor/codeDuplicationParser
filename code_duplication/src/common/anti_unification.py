from .PatternNode import PatternNode


def anti_unify(list1, list2, index1, index2, worktable):
    # mark the pair as checked/True <-- really necessary??
    worktable[index1][index2] = True
    # determine if subtrees are the same (and lengths same)
    if list1 == list2:  # if true:
        # check if leaves
        if not list1[index1].child_indices and not list2[index2].child_indices:
            t = PatternNode(list1[index1], list2[index2], list1[index1].weight, list1[index1].value)
            return t
        else:  # if not leaves:
            # iterate thru node's children, adding them as new children to the new fake node
            p = PatternNode(list1[index1], list2[index2], list1[index1].weight, list1[index1].value)
            for c in list1[index1].child_indices:
                # call function on children to get their subtrees - DFS???
                # RECURSION
                subtree = anti_unify(list1, list2, c, c, worktable)
                # associate with p
                p.add_children(subtree)
            return p
    else:  # if false:
        # return hole with combined weights
        weights = [list1[index1].weight, list2[index2].weight]
        temp = PatternNode(list1[index1], list2[index2], weights)
        return temp
