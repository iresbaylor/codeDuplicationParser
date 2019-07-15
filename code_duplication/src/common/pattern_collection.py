"""
Compares two Abstract Syntax Trees representing two methods
"""


def pattern_collection(tree1, tree2, labels1, labels2):
    # Checks whether a pairing has been compared
    worklist = [[True] * len(labels2) for i in range(len(labels1))]
    # Get subtrees from function 1
    node_list_1 = tree1.funcdef.walk()
    # Get subtrees from function 2
    node_list_2 = tree2.funcdef.walk()

    # map of s to 2^p
    pats = [[] * (len(node_list_1) + len(node_list_2))]
    # map of s to 2^c
    cpats = [[] * (len(node_list_1) + len(node_list_2))]

    # for all subtrees that aren't leaf nodes
    for i in range(0, len(node_list_1)):
        for j in range(0, len(node_list_2)):
            # if worklist is true
            if worklist[i][j]:
                # set it to false
                worklist[i][j] = False
                # if the root nodes of the subtrees are equal
                if node_list_1[i].equals(node_list_2[j]):
                    # Add the results of anti-unify to the list of subtrees
                    pats[i].append(anti_unify(node_list_1[i], node_list_2[i], worklist))
    # for every node in the tree
    for i in range(0, len(pats)):
        # Run the clustering function on the pats of each element
        cpats.append(clustering(pats[i]))
    # Return the values of the clustering function
    return cpats


def anti_unify(subtree1, subtree2, worklist):
    return 0


def clustering(pattern):
    return 0
