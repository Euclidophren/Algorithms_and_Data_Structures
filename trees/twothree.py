class TwoThreeNode:
    def __init__(self,
                 parent=None,
                 count=0,
                 smallest=None,
                 largest=None,
                 left=None,
                 middle=None,
                 right=None
                 ):
        self.parent = parent
        self.count = count

        self.smallest = smallest
        self.largest = largest

        self.left = left
        self.middle = middle
        self.right = right

    def __lt__(self, other):
        if self.largest == other.largest:
            return self.smallest < other.smallest
        else:
            return self.largest < other.largest

    def __le__(self, other):
        if self.largest == other.largest:
            return self.smallest <= other.smallest
        else:
            return self.largest <= other.largest

    def __gt__(self, other):
        if self.largest == other.largest:
            return self.smallest > other.smallest
        else:
            return self.largest > other.largest

    def __ge__(self, other):
        if self.largest == other.largest:
            return self.smallest >= other.smallest
        else:
            return self.largest >= other.largest

    def __eq__(self, other):
        return (self.largest == other.largest and
                self.smallest == other.smallest)

    def __ne__(self, other):
        return (self.largest != other.largest or
                self.smallest != other.smallest)

    def __str__(self):
        return self.tree_to_str(self, "")

    @staticmethod
    def tree_to_str(node, indent=""):
        if is_interior(node):
            cargo = indent + "(v " + str(node.smallest) + \
                    " : ^ " + str(node.largest) + \
                    " : # " + str(node.count) + ')\n'
        else:
            return indent + str(node) + '\n'

        left = node.tree_to_str(node.left, indent + " |")
        middle = node.tree_to_str(node.middle, indent + " |")
        right = ""
        if has_three_children(node):
            right = node.tree_to_str(node.right, indent + " |")

        return cargo + left + middle + right

    def tree_to_list(self):
        if is_interior(self.left):
            if has_three_children(self):
                output = (self.left.tree_to_list() +
                          self.middle.tree_to_list() +
                          self.right.tree_to_list())
            else:
                output = (self.left.tree_to_list() +
                          self.middle.tree_to_list())
            return output
        else:
            if has_three_children(self):
                output = [self.left,
                          self.middle,
                          self.right]
            else:
                output = [self.left,
                          self.middle]
            return output

    def search(self, value, index):
        if is_interior(self.left):
            if value <= self.left.largest:
                return self.left.search(value, index)

            index += self.left.count
            if value <= self.middle.largest:
                return self.middle.search(value, index)

            index += self.middle.count
            if (has_three_children(self) and
                    value <= self.right.largest):
                return self.right.search(value, index)
            return None
        else:
            # do inserts based on values
            if value == self.left:
                return index

            index += 1
            if value == self.middle:
                return index

            index += 1
            if value == self.right:
                return index

            return None

    #########################
    # select implementation #
    #########################

    def select(self, index):
        if is_interior(self.left):
            if index < self.left.count:
                return self.left.select(index)

            index -= self.left.count
            if index < self.middle.count:
                return self.middle.select(index)

            index -= self.middle.count
            if (has_three_children(self) and
                    index < self.right.count):
                return self.right.select(index)
            else:
                return None
        else:
            if index == 0:
                return self.left
            elif index == 1:
                return self.middle
            else:
                return self.right

    def insert(self, value):
        if is_interior(self.left):
            if value <= self.left.largest:
                self.left.insert(value)
            elif (value <= self.middle.largest or
                  not has_three_children(self)):
                self.middle.insert(value)
            else:
                self.right.insert(value)
        else:
            if not has_three_children(self):
                self.pin_node(value)
            else:
                new_node = self.split_node(value)
                self.ripple_split(new_node)

    def ripple_split(self, overflow):
        if is_root(self):
            self.make_new_root(overflow)
            return
        else:
            current = self.parent

        if not has_three_children(current):
            current.pin_node(overflow)
            return
        else:
            new_node = current.split_node(overflow)
            current.ripple_split(new_node)

    def pin_node(self, overflow):
        if overflow <= self.left:
            self.right = self.middle
            self.middle = self.left
            self.left = overflow
        elif overflow <= self.middle:
            self.right = self.middle
            self.middle = overflow
        else:
            self.right = overflow

        if is_interior(self.left):
            self.count = self.left.count + self.middle.count + self.right.count
            self.smallest = self.left.smallest
            self.largest = self.right.largest

            overflow.parent = self
        else:
            self.count = 3
            self.smallest = self.left
            self.largest = self.right

        self.correct_heuristics()

    def split_node(self, overflow):
        temp = sorted([self.left, self.middle, self.right, overflow])
        self.left = temp[0]
        self.middle = temp[1]

        if is_interior(self.left):
            self.count = self.left.count + self.middle.count
            self.smallest = self.left.smallest
            self.largest = self.middle.largest
            new_node = TwoThreeNode(self.parent,
                                    temp[2].count + temp[3].count,
                                    temp[2].smallest, temp[3].largest,
                                    temp[2], temp[3], None)
            new_node.left.parent = new_node
            new_node.middle.parent = new_node

        else:
            self.count = 2
            self.smallest = self.left
            self.largest = self.middle
            new_node = TwoThreeNode(self.parent,
                                    2,
                                    temp[2], temp[3],
                                    temp[2], temp[3], None)
        self.right = None
        return new_node

    # creates a new root using two nodes as children
    # takes the old root and an addition node as the children

    def make_new_root(self, overflow):
        if is_interior(overflow):
            new_root = TwoThreeNode(None,
                                    self.count + overflow.count,
                                    self.smallest, overflow.largest,
                                    self, overflow, None)
        else:
            new_root = TwoThreeNode(None,
                                    self.count + overflow.count,
                                    self, overflow,
                                    self, overflow, None)
        self.parent = new_root
        overflow.parent = new_root

    def delete(self, value):
        if is_interior(self.left):
            if value <= self.left.largest:
                return self.left.delete(value)
            elif value <= self.middle.largest:
                return self.middle.delete(value)
            elif (has_three_children(self) and
                  value <= self.right.largest):
                return self.right.delete(value)
            else:  # the value does not exist in the tree
                return False
        else:
            if has_three_children(self):
                deleted = self.unpin_node(value)
                if deleted:
                    self.correct_heuristics()
                return deleted
            else:
                deleted = self.unpin_node(value)
                if deleted:
                    self.ripple_merge()
                return deleted

    def unpin_node(self, target):
        if target == self.left:
            self.left = self.middle
            self.middle = self.right
        elif target == self.middle:
            self.middle = self.right
        elif target == self.right:
            pass
        else:
            return False

        self.right = None
        self.smallest = self.left
        self.largest = self.middle
        self.count = 2

        return True

    def take_from_left(self, sibling):
        self.middle = self.left
        self.left = sibling.right
        if not is_leaf(self.left):
            self.left.parent = self
        sibling.right = None

        if not is_leaf(self.left):
            self.count = self.left.count + self.middle.count
            self.smallest = self.left.smallest
            self.largest = self.middle.largest

            sibling.count = sibling.left.count + sibling.middle.count
            sibling.smallest = sibling.left.smallest
            sibling.largest = sibling.middle.largest
        else:
            self.count = 2
            self.smallest = self.left
            self.largest = self.middle

            sibling.count = 2
            sibling.smallest = sibling.left
            sibling.largest = sibling.middle

    def take_from_right(self, sibling):
        self.middle = sibling.left
        if not is_leaf(self.middle):
            self.middle.parent = self
        sibling.left = sibling.middle
        sibling.middle = sibling.right
        sibling.right = None

        if not is_leaf(self.left):
            self.count = self.left.count + self.middle.count
            self.smallest = self.left.smallest
            self.largest = self.middle.largest

            sibling.count = sibling.left.count + sibling.middle.count
            sibling.smallest = sibling.left.smallest
            sibling.largest = sibling.middle.largest
        else:
            self.count = 2
            self.smallest = self.left
            self.largest = self.middle

            sibling.count = 2
            sibling.smallest = sibling.left
            sibling.largest = sibling.middle

    def ripple_merge(self):
        if is_root(self):
            if has_one_children(self):
                self.collapse_root()
            return
        else:
            current = self.parent

        if is_left_child(self):
            if has_three_children(current.middle):
                self.take_from_right(current.middle)
            else:
                current.middle.pin_node(self.left)
                current.left = current.middle
                current.middle = current.right
                current.right = None
        elif is_middle_child(self):
            if has_three_children(current.left):
                self.take_from_left(current.left)
            else:
                current.left.pin_node(self.left)
                current.middle = current.right
                current.right = None
        else:
            if has_three_children(current.middle):
                self.take_from_left(current.middle)
            else:
                current.middle.pin_node(self.left)
                current.right = None

        if has_one_children(current):
            current.ripple_merge()
        else:
            self.correct_heuristics()

    def collapse_root(self):
        self.left.parent = None

    def correct_heuristics(self):

        current = self.parent
        while is_interior(current):
            current.count = (current.left.count +
                             current.middle.count)
            current.smallest = current.left.smallest

            if has_three_children(current):
                current.count += current.right.count

            current.largest = current.middle.largest

            current = current.parent


def is_leaf(node):
    return type(node) is not TwoThreeNode


def is_interior(node):
    return type(node) is TwoThreeNode


def has_three_children(node):
    return node.right is not None


def has_two_children(node):
    return (node.right is None and
            node.middle is not None)


def has_one_children(node):
    return (node.right is None and
            node.middle is None and
            node.left is not None)


def is_left_child(node):
    return node.parent.left is node


def is_middle_child(node):
    return node.parent.middle is node


def is_right_child(node):
    return node.parent.right is node


def is_root(node):
    return node.parent is None


class TwoThreeTree:
    def __init__(self):
        self.root = None
        self.count = 0

    def __str__(self):
        return str(self.root)

    def structuredStr(self):
        return self.root.treeToStr(self.root, "")

    def insert(self, value):
        if self.count == 0:
            self.root = value
        elif self.count == 1:
            temp = self.root
            left = min(temp, value)
            middle = max(temp, value)
            self.root = TwoThreeNode(None,
                                     2,
                                     left, middle,
                                     left, middle, None)
        else:
            self.root.insert(value)
            if self.root.parent is not None:
                self.root = self.root.parent
        self.count += 1

    def delete(self, value):
        deleted = True
        if self.count == 0:
            deleted = False
        elif self.count == 1:
            if self.root == value:
                self.root = None
                deleted = True
            else:
                deleted = False
        elif self.count == 2:
            if self.root.left == value:
                self.root = self.root.middle
                deleted = True
            elif self.root.middle == value:
                self.root = self.root.left
                deleted = True
            else:
                deleted = False
        elif self.count == 3:
            deleted = self.root.unPinNode(value)
        else:
            deleted = self.root.delete(value)
            if self.root.left.parent is None:
                self.root = self.root.left

        if deleted:
            self.count -= 1
        return deleted

    def select(self, index):
        if index < 0:
            index = self.count + index

        if self.count == 1 and index == 0:
            return self.root
        else:
            return self.root.select(index)

    def __getitem__(self, index):
        return self.select(index)

    def search(self, value):
        if self.count == 1 and value == self.root:
            return self.root
        else:
            return self.root.search(value, 0)

    def min(self):
        return self.select(0)

    def max(self):
        return self.select(-1)
