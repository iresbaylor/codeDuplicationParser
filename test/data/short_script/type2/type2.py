MUL_COUNT = 2


def mul2(value):
    val_times2 = sum(value for _ in range(MUL_COUNT))
    return val_times2


def sum_times2(param1, param2):
    tmp1 = mul2(param1)
    tmp2 = (lambda y: mul2(y))(param2)
    return (lambda *params: sum(params))(tmp1, tmp2)


if __name__ == "__main__":
    VALUE_BASE = 16
    tmp = sum_times2(VALUE_BASE, VALUE_BASE << 1)
    print("Result:", tmp)
