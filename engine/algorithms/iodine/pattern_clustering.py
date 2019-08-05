def clustering(ps):
    """
    Perform pattern clustering and return clusters.

    Arguments:
        ps -- a set of patterns

    Returns:
        a set of clustered-patterns

    """
    cs = []  # initialize the set
    for p in ps:  # iterate through the patterns in the set of patterns
        merged = False
        for c in cs:  # iterate through the clustered-patterns in the set of clustered-patterns
            # if the pattern and the clustered-pattern are the same shape
            if p.skeleton_equals(c):
                c.add_node(p)  # merge labels of p into c
                merged = True
                break
        if not merged:
            cs.append(p)
    return cs
