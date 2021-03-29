# def digit(number: int, pos: int) -> int:
#
#
# def radix_sort_lsd(array: list, m: int) -> list:
#     n = len(array) - 1
#     for i in range(1, m + 1):
#         for j in range(k):
#             c[j] = 0
#         for j in range(n):
#             d = digit(array[j], i)
#             c[d] += 1
#         count = 0
#         for j in range(k - 1):
#             tmp = c[j]
#             c[j] = count
#             count += tmp
#         for j in range(n):
#             d = digit(array[j], i)
#             b[c[d]] = array[j]
#             c[d] += 1
#         array = b
#     return array
#
#
# def radix_sort_msd(array: list, l: int, r: int, d: int) -> list:
#     if d > m or l >= r:
#         return
#     for j in range(k + 2):
#         cnt[j] = 0
#     for i in (l, r):
#          j = digit(array[i], d)
#          cnt[j + 1] += 1
#     for j in range(2, k + 1):
#         cnt[j] += cnt[j - 1]
#     for i in range(l, r + 1):
#         j = digit(array[i], d)
#         c[l + cnt[j]] = array[i]
#         cnt[j] -= 1
#     for i in range(l, r + 1):
#         array[i] = c[i]
#     radix_sort_msd((array. l, l + cnt[0] - 1, d + 1))
#     for i in range(1, k + 1):
#         radix_sort_msd(array, l + cnt[i - 1], l + cnt[i] - 1, d + 1)


# Rosetta code implementation
def flatten(l):
    return [y for x in l for y in x]


def radix(l, p=None, s=None):
    if s is None:
        s = len(str(max(l)))
    if p is None:
        p = s
    i = s - p
    if i >= s:
        return l
    bins = [[] for _ in range(10)]
    for e in l:
        bins[int(str(e).zfill(s)[i])] += [e]
    return flatten([radix(b, p - 1, s) for b in bins])
