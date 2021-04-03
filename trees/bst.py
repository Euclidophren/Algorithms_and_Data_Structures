# class Node:
#     def __init__(self, left, right, parent, node_key):
#         self.left = left
#         self.right = right
#         self.parent = parent
#         self.node_key = node_key
#
#
# class BinaryTree:
#     def __init__(self, tree_root=None):
#         self.tree_root = tree_root
#
#     def inorder_traversal(self, curr_node):
#         if curr_node:
#             self.inorder_traversal(curr_node.left)
#             print(curr_node.node_key)
#             self.inorder_traversal(curr_node.right)
#
#     def preorder_traversal(self, curr_node):
#         if curr_node:
#             print(curr_node.node_key)
#             self.inorder_traversal(curr_node.left)
#             self.inorder_traversal(curr_node.right)
#
#     def postorder_traversal(self, curr_node):
#         if curr_node:
#             self.inorder_traversal(curr_node.left)
#             self.inorder_traversal(curr_node.right)
#             print(curr_node.node_key)

#!/usr/bin/python


class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val


class Tree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if self.root is not None:
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if val == node.v:
            return node
        elif val < node.v and node.l is not None:
            return self._find(val, node.l)
        elif val > node.v and node.r is not None:
            return self._find(val, node.r)

    def delete_tree(self):
        self.root = None

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node is not None:
            self._print_tree(node.l)
            print(str(node.v) + ' ')
            self._print_tree(node.r)
