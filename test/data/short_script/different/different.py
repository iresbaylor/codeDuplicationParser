DOUBLE_COUNT = 4


def double(val):
    double_val = val / DOUBLE_COUNT
    return DOUBLE_COUNT + double_val


def double_sum(arg1, arg2):
    double1 = double(arg2)
    double2 = double(arg1)
    return double2 / double1


if __name__ == "__main__":
    BASE_VALUE = 12
    result = double_sum(BASE_VALUE, BASE_VALUE >> 1)
    print(result, "<- Result")
