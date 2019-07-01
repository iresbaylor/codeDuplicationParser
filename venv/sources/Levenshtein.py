# get minimum of three values
def minimum(val1, val2, val3):
    min = val1
    if val2 < min:
        min = val2
    if val3 < min:
        min = val3
    return min

# takes two words and determines levenshtein distance
def lev_distance(w1, w2):
    length1 = len(w1)+1 # length of word 1 - col
    length2 = len(w2)+1 # length of word 2 - row
    cost = 0            # cost

    # STEP 1
    # check if words are empty
    if length1-1 == 0 or length2-1 == 0:
        print("cannot compare words - empty")
        exit(1)

    # matrix thing
    m = [[0 for x in range(length1)] for y in range(length2)]

    # STEP 2
    # fill first row & col of matrix
    for x in range(length2):
        m[x][0] = x;

    for y in range(length1):
        m[0][y] = y;

    # STEP 3
    for x in range(1, length2):
        letter2 = w2[x-1]

        # STEP 4
        for y in range(1, length1):
            letter1 = w1[y-1]

            # STEP 5
            if letter1 == letter2:
                cost = 0
            else:
                cost = 1

            # STEP 6
            m[x][y] = min(m[x-1][y]+1, m[x][y-1]+1, m[x-1][y-1]+cost)

    # STEP 7
    return m[length2-1][length1-1]