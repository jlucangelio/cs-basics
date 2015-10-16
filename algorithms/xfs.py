from collections import deque

class node(object):
    def __init__(self, label, neighbours):
        self.label = label
        self.neighbours = neighbours

def xfs(node, b=True):
    q = deque()
    visited = set([])

    q.append(node)
    visited.add(node)
    while (len(q) > 0):
        if b:
            n = q.popleft()
        else:
            n = q.pop()

        print n.label

        for m in n.neighbours:
            if m not in visited:
                q.append(m)
                visited.add(m)


if __name__ == "__main__":
    n1 = node(1, [])
    n2 = node(2, [n1])
    n3 = node(3, [n1, n2])

    xfs(n3, True)
    print
    xfs(n3, False)
