import random
import warnings
from trees.bst import BSTNode, BST


class TreapNode(BSTNode):
    def __init__(self, data, priority=None):
        if priority is not None and type(priority) not in {int, float}:
            raise TypeError("Given priority has to be a number!!")
        super().__init__(data)
        self._priority = (
            random.randint(0, 100)
            if priority is None
            else priority
        )

    def get_priority(self):
        return self._priority

    def set_priority(self, new_priority):
        if type(new_priority) not in {int, float}:
            raise TypeError("Given priority has to be a number!!")
        self._priority = new_priority

    def __repr__(self):
        return f"TreapNode(data: {self._data}, Priority: {self._priority})"

    def _represent(self):
        if Treap.SHOW_PRIORITY:
            return f"{self._data}|P:{self._priority}"
        else:
            return f"{self._data}"


class Treap(BST):
    SHOW_PRIORITY = False
    _basic_node = TreapNode
    __name__ = "extra.Treap()"

    def __init__(self, iterable=None, seed=None):
        random.seed(seed)
        super().__init__(iterable)

    def __len__(self):
        return self._length

    def is_empty(self):
        return super().is_empty()

    def get_max(self):
        return super().get_max()

    def get_min(self):
        return super().get_min()

    def __contains__(self, find_val):
        return super().__contains__(find_val)

    def __validate_priority(self, new_priority):
        if new_priority is not None and type(new_priority) not in {int, float}:
            raise TypeError("Given priority has to be a number!!")

    def insert(self, value, priority=None):
        super()._validate_item(value)
        self.__validate_priority(priority)
        if self.is_empty():
            self._root = self._basic_node(value, priority)
            self._length += 1
        else:
            new_node = super()._insert_node(
                self._root, self._basic_node(value, priority)
            )
            parent = new_node.get_parent()
            while parent is not None:
                grandparent = parent.get_parent()
                if parent.get_priority() > new_node.get_priority():
                    break
                else:
                    if new_node.is_left_child():
                        parent = super()._rotate_right(parent)
                    else:
                        parent = super()._rotate_left(parent)
                    super()._attach(grandparent, parent)
                    new_node = parent
                    parent = grandparent

    # =============================    REMOVE    ==============================
    def remove(self, del_value):
        if self.is_empty():
            warnings.warn(f"`{self.__name__}` is empty!!", UserWarning)
            return
        elif type(del_value) not in {int, float}:
            warnings.warn(
                f"Couldn't find `{del_value}` in `{self.__name__}`!!",
                UserWarning
            )
            return
        elif self._root.is_leaf() and del_value == self._root.get_data():
            self._root = None
            self._length -= 1
        else:
            removed_node = super()._search(del_value, self._root)
            if removed_node.get_data() != del_value:
                warnings.warn(
                    f"Couldn't find `{del_value}` in `{self.__name__}`",
                    UserWarning
                )
                return
            parent = removed_node.get_parent()
            while not removed_node.is_leaf():
                left_child = removed_node.get_left()
                right_child = removed_node.get_right()
                left_priority = left_child.get_priority() if left_child else -1
                right_priority = (
                    right_child.get_priority()
                    if right_child
                    else -1
                )
                # perform rotation
                if left_priority > right_priority:
                    removed_node = super()._rotate_right(removed_node)
                    super()._attach(parent, removed_node)
                    parent = removed_node
                    removed_node = parent.get_right()
                else:
                    removed_node = super()._rotate_left(removed_node)
                    super()._attach(parent, removed_node)
                    parent = removed_node
                    removed_node = parent.get_left()
            if removed_node.is_left_child():
                parent.set_left(None)
            else:
                parent.set_right(None)
            self._length -= 1

    def clear(self):
        super().clear()

    def get_height(self):
        return super().get_height()

    def get_depth(self):
        return super().get_depth()

    def count_leaf_nodes(self):
        return super().count_leaf_nodes()

    def is_balanced(self):
        return super().is_balanced()

    def is_perfect(self):
        return super().is_perfect()

    def is_strict(self):
        return super().is_strict()

    def __iter__(self):
        return super().__iter__()

    def to_list(self):
        return super().to_list()

    def get_nodes_per_level(self):
        return super().get_nodes_per_level()

    def preorder_traverse(self):
        return super().preorder_traverse()

    def depth_first_traverse(self):
        return super().depth_first_traverse()

    def postorder_traverse(self):
        return super().postorder_traverse()

    def inorder_traverse(self):
        return super().inorder_traverse()

    def breadth_first_traverse(self):
        return super().breadth_first_traverse()

    def traverse(self, method="inorder"):
        return super().traverse(method)
