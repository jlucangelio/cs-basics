def matches1(pattern, string):
    seen = set()
    plen = len(pattern)
    slen = len(string)

    matched = set([(0, 0)])
    while len(matched) > 0:
        new_matched = set()

        for pi, si in matched:
            if (pi, si) in seen:
                continue

            if pi == plen and si == slen:
                return True

            if pi < plen:
                pe = pattern[pi]

                if pe == "*":
                    new_matched.add((pi + 1, si))
                    if si < slen:
                        new_matched.add((pi, si + 1))
                        new_matched.add((pi + 1, si + 1))
                else:
                    if si < slen and (pe == "?" or pe == string[si]):
                        new_matched.add((pi + 1, si + 1))

        seen.update(matched)
        matched = new_matched

    return False


def matches2(pattern, string):
    pass


def test(f):
    print f("", ""), True
    print f("*", ""), True
    print f("", "a"), False
    print f("a", "a"), True
    print f("a", "b"), False
    print f("ab", "ab"), True
    print f("a?c", "abc"), True
    print f("a*c", "abc"), True
    print f("a*c", "ac"), True
    print f("a*b", "abbbb"), True
    print f("a*b*c", "abbbbc"), True
    print f("a*b*c", "abbbbcd"), False
    print f("a*bc*bc", "abbbbcbc"), True
    print f("a*a*a*", "aaaaaa"), True
    print


if __name__ == "__main__":
    test(matches1)
    # print matches1("a*" * 1000, "a" * 2000)
