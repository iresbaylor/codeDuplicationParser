def main():
    print("first 10 fibonacci numbers")
    for i in range(1, 10):
        print(fibonacci(i))

    print("that's a lot of fibonacci")


def fibonacci(i):
    if i > 0:
        return fibonacci(i - 1) + fibonacci(i - 2)

