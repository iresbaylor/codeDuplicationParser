# takes two words and determines levenshtein distance
def lev_distance(w1, w2):
    length1 = len(w1)   # length of word 1
    length2 = len(w2)   # length of word 2
    cost = 0            # cost

    # check if words are empty
    if length1 == 0 or length2 == 0:
        print("cannot compare words - empty")
        exit(1)

    # matrix