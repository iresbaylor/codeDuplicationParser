def hello(param1="Wor", arg2="ld!"):
    """The `hello()` source function."""
    combined_args = param1 + arg2

    prefix = "Hello"
    prefix += ","

    print(prefix, combined_args)
