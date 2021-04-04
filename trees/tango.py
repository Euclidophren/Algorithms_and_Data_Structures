from splay import SplayTree
from BST import BalancedTree


class TangoTree:
    def __init__(self, nodes):
        self.repre = BalancedTree(nodes).root

    def access(self, key):  # searching
        depth = 0
        start, cur = self.repre, self.repre
        if start.aux is None:
            aux_path = SplayTree()
            while True:
                if cur != self.repre:
                    cur.marked = False
                aux_path.insert(cur)
                if key == cur.key:
                    print("Found: " + str(cur.key) + " Depth:" + str(depth))
                    break
                elif key < cur.key:
                    cur = cur.repreLeft
                else:
                    cur = cur.repreRight
                depth += 1
            self.repre.aux = aux_path
            return
        else:
            cur_aux = self.repre.aux
            to_link = None
            cur_key, parent_key = self.repre.key, self.repre.key
            while True:
                cur_key = cur.key
                if cur.aux:
                    cur_aux = cur.aux
                    find = cur_aux.find(key)  # search in splay tree
                    cur = find[0]
                    depth += find[1]
                    if to_link:  # link it to preferred path from root
                        self.join(start.aux, cur.aux, parent_key, cur_key)
                        cur.aux = None
                        cur.marked = False
                elif cur.marked:
                    start.aux.insert(cur)
                    cur.marked = False
                if cur.key == key:
                    print("Found: " + str(cur.key) + " Depth:" + str(depth))
                    return
                elif cur.key > key:
                    to_link = cur.repreLeft
                    to_cut = cur.repreRight
                else:
                    to_link = cur.repreRight
                    to_cut = cur.repreLeft
                if to_cut and to_cut.marked == False:
                    cut_res = self.cut(cur_aux, to_cut)
                    start.aux = cut_res[0]
                    to_cut.marked = True
                    to_cut.aux = cut_res[1]
                depth += 1

                parent_key = cur.key
                cur, to_link = to_link, start.aux

    def cut(self, splayTree, node):
        """
        :param x:
        :return: None
        """
        f = self.findMinMaxInSub(node)
        minV = f[0]
        maxV = f[1]
        smaller = splayTree.split(minV, True)
        # print smaller.traversal_test()
        # print splayTree.traversal_test()
        larger = splayTree.split(maxV, False)
        # print larger.traversal_test()
        # print splayTree.traversal_test()
        cutoff = splayTree
        if not smaller.root:
            splayTree = larger
        else:
            smaller.join(larger)
            splayTree = smaller
        # print splayTree.traversal_test()
        return (splayTree, cutoff)

    def findMinMaxInSub(self, node):
        minV, maxV = node.key, node.key
        cur = node
        while cur:
            if cur.repreLeft and cur.repreLeft.marked == False:
                minV = min(minV, cur.repreLeft.key)
                maxV = max(maxV, cur.repreLeft.key)
                cur = cur.repreLeft
            elif cur.repreRight and cur.repreRight.marked == False:
                minV = min(minV, cur.repreRight.key)
                maxV = max(maxV, cur.repreRight.key)
                cur = cur.repreRight
            else:
                break
        return (minV, maxV)

    # def update(self):

    def join(self, S1, S2, x1, x2):
        if x1 > x2:
            rootV = S1.findMax()
            S1.splay(rootV)
            S1.root.left = S2
        else:
            rootV = S1.findMin()
            S1.splay(rootV)
            S1.root.right = S2
