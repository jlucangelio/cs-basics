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


# Sketch of a different way to solve the problem. Uses str.find() and
# str.rfind() as a shortcut and so doesn't support '?'. Is significantly faster.
def matches2(pattern, string):
    if len(pattern) == 0 and len(string) == 0:
        return True
    if len(pattern) == 0:
        return False

    sindex = 0
    chunks = pattern.split("*") # O(n)
    num_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        if len(chunk) == 0:
            # Consecutive '*'s, or trailing '*'.
            continue

        no_star_before = i == 0 # first chunk
        no_star_after = i == num_chunks - 1 or num_chunks == 1 # last chunk or only chunk

        chunk_start_index = -1
        if no_star_before:
            if not string.startswith(chunk):
                return False
            chunk_start_index = 0
        elif no_star_after:
            chunk_start_index = string.rfind(chunk, sindex)
        else: # star_before and star_after
            chunk_start_index = string.find(chunk, sindex)

        if chunk_start_index < 0:
            return False

        sindex = chunk_start_index + len(chunk)

        if no_star_after and sindex < len(string):
            return False

    return True


# Dynamic programming.
def matches3(pattern, string):
    plen = len(pattern)
    slen = len(string)

    nrows = plen + 1
    ncols = slen + 1

    # partial[i][j] == pattern[:i] matches string[:j]
    partial = [[None for _ in range(ncols)] for _ in range(nrows)]

    # Empty |pattern| matches empty |string|.
    partial[0][0] = True
    # Empty |pattern| doesn't match non-empty |string|.
    for colindex in range(1, ncols):
        partial[0][colindex] = False

    for rowindex in range(1, nrows):
        # If we enter the loop, nrows > 1 => plen + 1 > 1 => plen > 0 =>
        # |pattern| is non-empty.
        pe = pattern[rowindex - 1]
        # Non-empty |pattern| matches empty |string| iff |pattern| is all stars.
        partial[rowindex][0] = pe == "*" and partial[rowindex - 1][0]

        for colindex in range(1, ncols):
            # If we enter the loop, ncols > 1 => slen + 1 > 1 => slen > 0 =>
            # |string| is non-empty.
            se = string[colindex - 1]

            if pe == "*":
                # 'pattern*' matches 'string<c>' iff:
                #   'pattern' matches 'string<c>' (star matches no characters)
                #   or 'pattern' matches 'string' (star matches at least one character)
                #   or 'pattern*' matches 'string' (star matches more than one character)
                partial[rowindex][colindex] = (partial[rowindex - 1][colindex]
                                               or partial[rowindex - 1][colindex - 1]
                                               or partial[rowindex][colindex - 1])
            elif pe == se or pe == "?":
                partial[rowindex][colindex] = partial[rowindex - 1][colindex - 1]
            else: # pe != se
                partial[rowindex][colindex] = False

    return partial[plen][slen]


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
    print f("a*b", "abbb"), True
    print f("a*b*c", "abbbbc"), True
    print f("a*b*c", "abbbbcd"), False
    print f("a*bc**bc", "abbbbcbc"), True
    print f("a*a*a*", "aaaaaa"), True
    print


if __name__ == "__main__":
    import datetime
    # test(matches1)
    # test(matches2)
    # test(matches3)

    print datetime.datetime.now()
    print matches1("a*" * 1000, "a" * 2000)
    print datetime.datetime.now()
    print matches2("a*" * 1000, "a" * 2000)
    print datetime.datetime.now()
    print matches3("a*" * 1000, "a" * 2000)
    print datetime.datetime.now()
