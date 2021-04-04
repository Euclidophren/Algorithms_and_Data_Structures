import math


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.key)


class ScapeGoatTree():
    def __init__(self, a):
        self.a = a
        self.size = 0
        self.max_size = 0
        self.root = None

    def size_of(self, x):
        if x is None:
            return 0
        return 1 + self.size_of(x.left) + self.size_of(x.right)

    def haT(self):
        return math.floor(math.log(self.size, 1.0 / self.a))

    def is_deep(self, depth):
        return depth > self.haT()

    @staticmethod
    def brother_of(node, parent):
        if parent.left is not None and parent.left.key == node.key:
            return parent.right
        return parent.left

    @staticmethod
    def my_rebuild_tree(root, length):
        def flatten(node, nodes):
            if node is None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def build_tree_from_sorted_list(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key)
            node.left = build_tree_from_sorted_list(nodes, start, mid - 1)
            node.right = build_tree_from_sorted_list(nodes, mid + 1, end)
            return node

        nodes = []
        flatten(root, nodes)
        return build_tree_from_sorted_list(nodes, 0, length - 1)

    @staticmethod
    def minimum(x):
        while x.left is not None:
            x = x.left
        return x

    def delete(self, delete_me):
        node = self.root
        parent = None
        is_left_child = True
        while node.key != delete_me:
            parent = node
            if delete_me > node.key:
                node = node.right
                is_left_child = False
            else:
                node = node.left
                is_left_child = True

        successor = None
        if node.left is None and node.right is None:
            pass
        elif node.left is None:
            successor = node.right
        elif node.right is None:
            successor = node.left
        else:
            successor = self.minimum(node.right)
            if successor == node.right:
                successor.left = node.left
            else:
                successor.left = node.left
                tmp = successor.right
                successor.right = node.right
                node.right.left = tmp

        if parent is None:
            self.root = successor
        elif is_left_child:
            parent.left = successor
        else:
            parent.right = successor

        self.size -= 1
        if self.size < self.a * self.max_size:
            # print "Rebuilding the whole tree"
            self.root = self.my_rebuild_tree(self.root, self.size)
            self.max_size = self.size

    def search(self, key):
        x = self.root
        while x is not None:
            if x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            else:
                return x

        return None

    def insert(self, key):
        z = Node(key)
        y = None
        x = self.root
        depth = 0
        parents = []
        while x is not None:
            parents.insert(0, x)
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
            depth += 1

        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1
        self.max_size = max(self.size, self.max_size)

        if self.is_deep(depth):
            scapegoat = None
            parents.insert(0, z)
            sizes = [0] * len(parents)
            I = 0
            for i in range(1, len(parents)):
                sizes[i] = sizes[i - 1] + self.size_of(self.brother_of(parents[i - 1], parents[i])) + 1
                if not self.is_weight_balanced(parents[i], sizes[i] + 1):
                    scapegoat = parents[i]
                    I = i

            tmp = self.my_rebuild_tree(scapegoat, sizes[I] + 1)

            scapegoat.left = tmp.left
            scapegoat.right = tmp.right
            scapegoat.key = tmp.key

    def is_weight_balanced(self, x, size_of_x):
        a = self.size_of(x.left) <= (self.a * size_of_x)
        b = self.size_of(x.right) <= (self.a * size_of_x)
        return a and b

    def preorder(self, x):
        if x is not None:
            print(x.key)
            self.preorder(x.left)
            self.preorder(x.right)

    def print_tree(self):
        self.preorder(self.root)
