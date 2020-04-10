def calculate_rc_constants(data):
    # at bats
    ab = get_val(data, "AB")
    # hits
    h = get_val(data, "H")
    # doubles
    two_b = get_val(data, "2B")
    # triples
    three_b = get_val(data, "3B")
    # home runs
    hr = get_val(data, "HR")
    # singles
    one_b = h - two_b - three_b - hr
    # stolen bases
    sb = get_val(data, "SB")
    # caught stealing
    cs = get_val(data, "CS")
    # base on balls
    bb = get_val(data, "BB")
    # intentional walks
    ibb = get_val(data, "IBB")
    # hit by pitch
    hbp = get_val(data, "HBP")
    # sacrifice hits
    sh = get_val(data, "SH")
    # sacrifice flies
    sf = get_val(data, "SF")
    # grounded into double plays
    gidp = get_val(data, "GIDP")

    tb = one_b + (2 * two_b) + (3 * three_b) + (4 * hr)
    s1 = h + bb - cs + hbp - gidp
    s2 = bb - ibb + hbp
    s3 = sh + sf + sb
    s4 = ab + bb + hbp + sf + sh

    return tb, s1, s2, s3, s4


def calculate_rc27(data, rc):
    # at bats
    ab = get_val(data, "AB")
    # hits
    h = get_val(data, "H")
    # caught stealing
    cs = get_val(data, "CS")
    # sacrifice hits
    sh = get_val(data, "SH")
    # sacrifice flies
    sf = get_val(data, "SF")
    # grounded into double plays
    gidp = get_val(data, "GIDP")

    outs = ab - h + sf + sh + gidp + cs
    if outs == 0:
        return 0

    return (rc * 27) / outs


def calculate_rc_base(data):
    b = 1
    c = 0.26
    d = 0.52
    return calculate_rc(data, b, c, d)


def calculate_rc(data, b, c, d):
    tb, s1, s2, s3, s4 = calculate_rc_constants(data)

    if s4 == 0:
        return 0
    return (s1 * (tb * b + (c * s2)) + (d * s3)) / s4


def get_val(data, index, default=0):
    return data[index] if index in data else default
