from random import randint, randrange


class Node:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, t):
        self.root = Node(True)
        self.t = t

    def print_tree(self, x, lvl=0):
        print("Level ", lvl, " --> ", len(x.keys), end=": ")
        for i in x.keys:
            print(i, end=" ")
        print()
        lvl += 1
        if len(x.children) > 0:
            for i in x.children:
                self.print_tree(i, lvl)

    def search(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i][0]:
                i += 1
            if i < len(x.keys) and k == x.keys[i][0]:
                return x, i
            elif x.leaf:
                return None
            else:
                return self.search(k, x.children[i])
        else:
            return self.search(k, self.root)

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = Node()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = Node(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t - 1]

    def delete(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k[0] > x.keys[i][0]:
            i += 1
        if x.leaf:
            if i < len(x.keys) and x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return
        if i < len(x.keys) and x.keys[i][0] == k[0]:
            return self._delete_internal_node(x, k, i)
        elif len(x.children[i].keys) >= t:
            self.delete(x.children[i], k)
        else:
            if i != 0 and i + 2 < len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    self._delete_sibling(x, i, i - 1)
                elif len(x.children[i + 1].keys) >= t:
                    self._delete_sibling(x, i, i + 1)
                else:
                    self._delete_merge(x, i, i + 1)
            elif i == 0:
                if len(x.children[i + 1].keys) >= t:
                    self._delete_sibling(x, i, i + 1)
                else:
                    self._delete_merge(x, i, i + 1)
            elif i + 1 == len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    self._delete_sibling(x, i, i - 1)
                else:
                    self._delete_merge(x, i, i - 1)
            self.delete(x.children[i], k)

    def _delete_internal_node(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        if len(x.children[i].keys) >= t:
            x.keys[i] = self._delete_predecessor(x.children[i])
            return
        elif len(x.children[i + 1].keys) >= t:
            x.keys[i] = self._delete_sucessor(x.children[i + 1])
            return
        else:
            self._delete_merge(x, i, i + 1)
            self._delete_internal_node(x.children[i], k, self.t - 1)

    def _delete_predecessor(self, x):
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.children[n].keys) >= self.t:
            self._delete_sibling(x, n + 1, n)
        else:
            self._delete_merge(x, n, n + 1)
        self._delete_predecessor(x.children[n])

    def _delete_sucessor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.children[1].keys) >= self.t:
            self._delete_sibling(x, 0, 1)
        else:
            self._delete_merge(x, 0, 1)
        self._delete_sucessor(x.children[0])

    def _delete_merge(self, x, i, j):
        cNode = x.children[i]
        if j > i:
            rsNode = x.children[j]
            for k in range(len(rsNode.keys)):
                cNode.keys.append(rsNode.keys[k])
                if len(rsNode.children) > 0:
                    cNode.children.append(rsNode.children[k])
            if len(rsNode.children) > 0:
                cNode.children.append(rsNode.children.pop())
            new = cNode
            x.keys.pop(i)
            x.children.pop(j)
        else:
            lsNode = x.children[j]
            lsNode.keys.append(x.keys[j])
            for i in range(len(cNode.keys)):
                lsNode.keys.append(cNode.keys[i])
                if len(lsNode.children) > 0:
                    lsNode.children.append(cNode.children[i])
            if len(lsNode.children) > 0:
                lsNode.children.append(cNode.children.pop())
            new = lsNode
            x.keys.pop(j)
            x.children.pop(i)
        if x == self.root and len(x.keys) == 0:
            self.root = new

    @staticmethod
    def _delete_sibling(x, i, j):
        cNode = x.children[i]
        if i < j:
            rsNode = x.children[j]
            cNode.keys.append(x.keys[i])
            x.keys[i] = rsNode.keys[0]
            if len(rsNode.children) > 0:
                cNode.children.append(rsNode.children[0])
                rsNode.children.pop(0)
            rsNode.keys.pop(0)
        else:
            lsNode = x.children[j]
            cNode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsNode.keys.pop()
            if len(lsNode.children) > 0:
                cNode.children.insert(0, lsNode.children.pop())


def main():
    B = BTree(3)

    # Insert
    customNo = 10
    for i in range(customNo):
        B.insert((i, randint(i, 5 * i)))
    B.print_tree(B.root)
    print()

    # Delete
    toDelete = randint(0, customNo)
    print("Key {} deleted!".format(toDelete))
    B.delete(B.root, (toDelete,))
    # B.delete(B.root, (4,))
    B.print_tree(B.root)
    print()

    # Search
    toSearch = randrange(0, 2 * customNo)
    if B.search(toSearch) is not None:
        print("Key {} found!".format(toSearch))
    else:
        print("Key {} not found!".format(toSearch))


# Program starts here
if __name__ == '__main__':
    main()