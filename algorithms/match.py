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
            chunk_start_index = string.rfind(chunk)
        else: # star_before and star_after
            chunk_start_index = string.find(chunk)

        if chunk_start_index < 0:
            return False

        sindex = chunk_start_index + len(chunk)

        if no_star_after and sindex < len(string):
            return False

    return True


def test(f):
    print f("", ""), True
    print f("*", ""), True
    print f("", "a"), False
    print f("a", "a"), True
    print f("a", "b"), False
    print f("ab", "ab"), True
    # print f("a?c", "abc"), True
    print f("a*c", "abc"), True
    print f("a*c", "ac"), True
    print f("a*b", "abbbb"), True
    print f("a*b*c", "abbbbc"), True
    print f("a*b*c", "abbbbcd"), False
    print f("a*bc**bc", "abbbbcbc"), True
    print f("a*a*a*", "aaaaaa"), True
    print


if __name__ == "__main__":
    import datetime
    test(matches1)
    test(matches2)

    print datetime.datetime.now()
    print matches1("a*" * 100, "a" * 200)
    print datetime.datetime.now()
    print matches2("a*" * 4000, "a" * 8000)
    print datetime.datetime.now()
