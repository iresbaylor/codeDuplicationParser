import tokenize


def then_there_were_tokens():
    filename = './sources/Levenshtein.py'
    with open(filename, 'rb') as f:
        for five_tuple in tokenize.tokenize(f.readline):
            print("---------------------")
            print(five_tuple)
            # print(five_tuple.type)
            # print(five_tuple.string)
            # print(five_tuple.start)
            # print(five_tuple.end)
            # print(five_tuple.line)