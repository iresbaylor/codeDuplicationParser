# get minimum of three values
def minimum(val1, val2, val3):
    mini = val1
    if val2 < mini:
        mini = val2
    if val3 < mini:
        mini = val3
    return mini


# takes two words and determines levenshtein distance
def lev_distance(line1, line2):
    # check if same kind of token
    ss1 = line1[15:17]
    ss2 = line2[15:17]

    if ss1 == ss2:
        # grab the strings
        i = line1.find("string='")
        j = line1.find("',")
        w1 = line1[i+8:j]
        i = line2.find("string='")
        j = line2.find("',")
        w2 = line2[i+8:j]

        # THE ACTUAL LEVENSHTEIN ALGORITHM
        length1 = len(w1)+1     # length of word 1 - col
        length2 = len(w2)+1     # length of word 2 - row

        # STEP 1
        # check if words are empty
        if length1-1 == 0 or length2-1 == 0:
            print("cannot compare things - empty")
            exit(1)

        # matrix thing
        m = [[0 for x in range(length1)] for y in range(length2)]

        # STEP 2
        # fill first row & col of matrix
        for x in range(length2):
            m[x][0] = x

        for y in range(length1):
            m[0][y] = y

        # STEP 3
        for x in range(1, length2):

            # STEP 4
            for y in range(1, length1):

                # STEP 5
                if w1[y-1] == w2[x-1]:
                    cost = 0
                else:
                    cost = 1

                # STEP 6
                m[x][y] = min(m[x-1][y]+1, m[x][y-1]+1, m[x-1][y-1]+cost)

        # STEP 7
        return m[length2-1][length1-1]
    else:
        # returns 3 bc they're definitely not the same
        return 3


# takes two lists and compares everything in them to everything in the other one
def list_compare(list1, list2):
    un = 0
    for x in list1:
        for y in list2:
            # calculate levenshtein
            dist = lev_distance(x, y)
            # determine if distance within acceptable threshold
            if dist >= 3:
                un = un+1

    # calculate percentage of similarity
    print(un/len(list2)*100)
