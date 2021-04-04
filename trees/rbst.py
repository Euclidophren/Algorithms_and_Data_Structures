import random


class Node:
    def __init__(self, key: int):
        self.key = key
        self.size = 1
        self.left = None
        self.right = None


class RandomizedBST:
    def __init__(self):
        self.root = None

    def empty(self):
        return self.root is None

    def _member(self, t, k):
        if t is None:
            return False
        elif k < t.key:
            return self._member(t.left, k)
        elif k > t.key:
            return self._member(t.right, k)
        else:
            return True

    def member(self, k):
        return self._member(self.root, k)

    @staticmethod
    def _size(t):
        return t.size if t is not None else 0

    @staticmethod
    def _new_node(k):
        return Node(k)

    def _fix_size(self, t):
        t.size = 1 + self._size(t.left) + self._size(t.right)

    def leaf_insert(self, t, k):
        if t is None:
            return self._new_node(k)
        elif k < t.key:
            t.left = self.leaf_insert(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self.leaf_insert(t.right, k)
            self._fix_size(t)
            return t
        else:
            return t

    def _rotate_right(self, d):
        b = d.left
        d.left = b.right
        b.right = d
        self._fix_size(d)
        self._fix_size(b)
        return b

    def _rotate_left(self, b):
        d = b.right
        b.right = d.left
        d.left = b
        self._fix_size(b)
        self._fix_size(d)
        return d

    def _root_insert(self, t, k):
        if t is None:
            return self._new_node(k)
        elif k < t.key:
            t.left = self._root_insert(t.left, k)
            return self._rotate_right(t)
        elif k > t.key:
            t.right = self._root_insert(t.right, k)
            return self._rotate_left(t)
        else:
            return t

    def _insert(self, t, k):
        if t is None:
            return self._new_node(k)
        elif random.randint(0, self._size(t) + 1) == 0:
            return self._root_insert(t, k)
        elif k < t.key:
            t.left = self._insert(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self._insert(t.right, k)
            self._fix_size(t)
            return t
        else:
            return t

    def insert(self, k):
        self.root = self._insert(self.root, k)

    def _join(self, t1, t2):
        if t1 is None:
            return t2
        elif t2 is None:
            return t1
        elif random.randint(0, self._size(t1) + self._size(t2)) < self._size(t1):
            t1.right = self._join(t1.right, t2)
            self._fix_size(t1)
            return t1
        else:
            t2.left = self._join(t1, t2.left)
            self._fix_size(t2)
            return t2

    def _delete(self, t, k):
        if t is None:
            return t
        elif k < t.key:
            t.left = self._delete(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self._delete(t.right, k)
            self._fix_size(t)
            return t
        else:
            return self._join(t.left, t.right)

    def delete(self, k):
        self.root = self._delete(self.root, k)

    def _tree_height(self, t):
        if t is None:
            return 0
        else:
            return 1 + max(self._tree_height(t.left), self._tree_height(t.right))

    def height(self):
        return self._tree_height(self.root)

    def print_tree(self):
        def rec(t, n_spaces):
            if t is None:
                return
            print(' ' * n_spaces, 'key:', t.key, 'size:', t.size, 'height:', self._tree_height(t))
            rec(t.left, n_spaces + 2)
            rec(t.right, n_spaces + 2)

        rec(self.root, 0)
