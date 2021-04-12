from sys import getsizeof


class Empty(object):
    pass


class Node:
    def __init__(self,
                 key,
                 m,
                 b_mask,
                 bm_mask,
                 sketch_gap,
                 sketch_maskl,
                 sketch_maskh
                 ):
        self.key = key
        self.children = []
        self.bs = []
        self.ms = []
        self.m = m
        self.b_mask = b_mask
        self.bm_mask = bm_mask
        self.sketch_gap = sketch_gap
        self.sketch_maskl = sketch_maskl
        self.sketch_maskh = sketch_maskh
        self.is_leaf = self.is_leaf()

    def is_leaf(self):
        return len(self.children) == 0


class FusionTree:
    def __init__(self, root):
        self.root = Node(key=self.max_keys)
        w = getsizeof(Empty()) * 8
        self.max_keys = int(pow(w, .2))
        if self.max_keys < 2:
            raise ValueError(f"Fusion trees need word size at least 32. Size was {self.max_keys}")
        self.min_keys = self.max_keys // 2
        self.root.is_leaf = True

    @staticmethod
    def precompute_node(x):
        if x.n == 0:
            return
        x.bs = get_impor_bits(x.keys)
        x.ms = get_m(x.bs, x.m)
        x.b_mask = get_mask(x.bs)
        x.bm_mask = get_combo_mask(x.bs, x.ms)
        x.sketch_gap = x.bs[len(x.bs) - 1] + x.ms[len(x.ms) - 1] - x.bs[0] - x.ms[0]
        x.sketch_gap = x.sketch_gap if x.sketch_gap == 0 else 1

        size = x.n
        for j in range(size):
            sketch = approx_sketch(x.m, x.keys[size - j - 1], x.b_mask, x.bm_mask, x.bs[0] + x.ms[0])
            x.sketches |= (sketch | 1 << x.sketch_gap) << j * (x.sketch_gap + 1)
            x.sketch_maskl |= (1 << j * (x.sketch_gap + 1))
            x.sketch_maskh |= (1 << x.sketch_gap) << j * (x.sketch_gap + 1)
            
    def split_child(self, x, i):
        z = [None] * self.max_keys
        y = x.children[i]
        z.is_leaf = y.is_leaf

        pivot = self.max_keys // 2
        z.n = self.max_keys - pivot - 1

        for j in range(z.n):
            z.keys[j] = y.keys[pivot + j]

        if y.is_leaf is not True:
            for j in range(z.n + 2):
                z.children[j] = y.children[pivot + j + 1]

        y.n = self.max_keys - z.n - 1

        x.children.insert(i + 1, z)
        x.children.pop(len(x.children) - 1)

        x.keys.insert(i, y.keys[pivot])
        x.keys.pop(len(x.keys) - 1)

        x.n += 1

    def insert_non_full(self, x, k):
        i = x.n
        if x.is_leaf:
            while i >= 1 and k < x.keys[i - 1]:
                x.keys[i] = x.keys[i - 1]
                i -= 1
            x.keys[i] = k
            x.n += 1
        else:
            while i >= 1 and k < x.keys[i - 1]:
                i -= 1
            i += 1
            if x.children[i - 1].n == self.max_keys:
                i += 1
            self.insert_non_full(x.children[i - 1], k)

    def successor(self, x, k):
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return x.keys[i]
        elif x.is_leaf():
            return x.keys[i]
        else:
            return self.successor(x.children[i], k)

    def fusion_successor(self, x, k):
        if x.n == 0:
            if x.is_leaf():
                return 0
            return self.fusion_successor(x.children[0], k)
        app_sketch = approx_sketch(x.m, k, x.b_mask, x.bm_mask, x.bs[0] + x.ms[0])
        repeat_sketch = app_sketch * x.sketch_maskl
        i1 = par_comp(x.sketches, repeat_sketch, x.sketch_maskh, x.sketch_maskl, x.n, x.sketch_gap)
        y = 0
        if i1 < x.n:
            lcp1 = k ^ x.keys[i1]

        
        