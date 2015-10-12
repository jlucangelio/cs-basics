import random

# Binary search tree. Unbalanced.

class Node(object):
    def __init__(self, value, left=None, right=None):
        self.v = value
        self.l = left
        self.r = right

    def min(self):
        if self.l:
            return self.l.min()
        else:
            return self.v

    def max(self):
        if self.r:
            return self.r.max()
        else:
            return self.v

    def is_bst(self):
        if not self.l and not self.r:
            return True

        is_left_bst = True
        is_right_bst = True
        if self.l:
            is_left_bst = self.l.is_bst() and self.v > self.l.max()
        if self.r:
            is_right_bst = self.r.is_bst() and self.v < self.r.min()

        return is_left_bst and is_right_bst

    def contains(self, value):
        if value == self.v:
            return True
        if self.l and value < self.v:
            return self.l.contains(value)
        if self.r and value > self.v:
            return self.r.contains(value)
        return False

    def insert(self, value):
        if value == self.v:
            return

        if value < self.v:
            if self.l:
                self.l.insert(value)
            else:
                self.l = Node(value, None, None)
        elif value > self.v:
            if self.r:
                self.r.insert(value)
            else:
                self.r = Node(value, None, None)


if __name__ == "__main__":
    one = Node(1, None, None)
    three = Node(3, None, None)
    two = Node(2, one, three)

    print two.is_bst(), "should be True"
    print two.contains(2), "should be True"

    five = Node(5, None, None)
    six = Node(6, five, None)

    four = Node(4, three, six)
    print four.is_bst(), "should be True"
    print four.contains(3), "should be True"

    four = Node(4, six, three)
    print four.is_bst(), "should be False"

    t = Node(random.randint(0, 1000000), None, None)

    for _ in range(1000):
        t.insert(random.randint(0, 1000000))

    print t.is_bst(), "should be True"
