def type1_check(modules):
    """
    Very simple type 1 code duplication check based on AST.dump() function.
    """

    WEIGHT_LIMIT = 25
    # PRIORITY_CLASSES = [ast.Module, ast.ClassDef,
    #                     ast.FunctionDef, ast.AsyncFunctionDef]

    node_dict = {}

    for m in modules:
        visited = set()

        for n in m:
            if n.parent_index in visited or n.weight < WEIGHT_LIMIT:
                visited.add(n.index)
                continue

            node_dump = n.dump()

            if node_dump in node_dict:
                visited.add(n.index)
                node_dict[node_dump].append(n)
            else:
                node_dict[node_dump] = [n]

    for v in node_dict.values():
        if len(v) > 1:
            log.success(v)
