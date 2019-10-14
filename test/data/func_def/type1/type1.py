

def hello(param1="Wor", arg2="ld!"):
    # This one has no docstring.
    combined_args = param1 + arg2
    prefix = "Hello"
    prefix += ","
    print(prefix, combined_args)
