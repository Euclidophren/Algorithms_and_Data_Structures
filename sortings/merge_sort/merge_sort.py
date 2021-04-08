def merge(array: list, left: int, mid: int, right: int):
    it1, it2 = 0, 0
    result = [None] * (right - left)

    while left + it1 < mid and mid + it2 < right:
        if array[left + it1] < array[mid + it2]:
            result[it1 + it2] = array[left + it1]
            it1 += 1
        else:
            result[it1 + it2] = array[mid + it2]
            it2 += 1

    while left + it1 < mid:
        result[it1 + it2] = array[left + it1]
        it1 += 1

    while mid + it2 < right:
        result[it1 + it2] = array[mid + it2]
        it2 += 1

    for i in range(it1 + it2):
        array[left + i] = result[i]


def merge_sort_recursive(array: list, left: int, right: int) -> list:
    if left + 1 >= right:
        return array
    mid = (left + right) // 2
    merge_sort_recursive(array, left, mid)
    merge_sort_recursive(array, mid, right)
    merge(array, left, mid, right)
    return array


def merge_sort_iterative(array: list) -> list:
    n, i = len(array), 1
    while i < n:
        for j in range(0, n - i, 2 * i):
            merge(array, j, j + i, min(j + 2 * i, n))
        i *= 2
    return array


if __name__ == '__main__':
    print(merge_sort_iterative([3, 4, 1, 5, -1, -3, 0]))
    print(merge_sort_recursive([3, 4, 1, 5, -1, -3, 0], 0, 7))
