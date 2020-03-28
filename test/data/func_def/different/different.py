def hello(param1="Wor", arg2="ld!"):
    """The `hello()` source function."""
    combined_args = arg2 + param1

    prefix = ","
    prefix += "Hello"

    print(combined_args, prefix)
