def partition(array: list, left: int, right: int) -> int:
    v = array[(left + right) // 2]
    i, j = left, right
    while i <= j:
        while array[i] < v:
            i += 1
        while array[j] > v:
            j -= 1
        if i >= j:
            break
        array[i + 1], array[j - 1] = array[j - 1], array[i + 1]
    return j


def quick_sort(array: list, left: int, right: int):
    if left < right:
        q = partition(array, left, right)
        quick_sort(array, left, q)
        quick_sort(array, q + 1, right)


if __name__ == '__main__':
    print(quick_sort([3, 4, 1, 5, -1, -3, 0], 0, 6))
