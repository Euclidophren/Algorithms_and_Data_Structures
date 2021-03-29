from collections import defaultdict


def counting_sort(array: list) -> list:
    min_elem, max_elem = min(array), max(array)
    count = defaultdict(int)
    for i in array:
        count[i] += 1
    result = []
    for j in range(min_elem, max_elem + 1):
        result += [j] * count[j]
    return result
