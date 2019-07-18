# returns a set of clustered-patterns
def clustering(ps):
    cs = set()  # initialize the set
    for p in ps:  # iterate through the patterns in the set of patterns
        merged = False
        for c in cs:  # iterate through the clustered-patterns in the set of clustered-patterns
            if p == c:  # if the pattern and the clustered-pattern are the same shape
                c.add_node(p)  # merge labels of p into c
                merged = True
                break
        if not merged:
            cs.Union(p)
    return cs
