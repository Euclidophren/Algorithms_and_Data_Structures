def selection_sort(array: list) -> list:
    n = len(array)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
    return array


def selection_sort_optimized(array: list) -> list:
    n = len(array)
    for i in range(n - 1):
        minimum = i
        for j in range(i + 1, n):
            if array[j] < array[minimum]:
                minimum = j
        array[i], array[minimum] = array[minimum], array[i]
    return array


if __name__ == '__main__':
    print(selection_sort([3, 4, 5, 7, 7, 1, -4, -5]))
    print(selection_sort_optimized([3, 4, 5, 7, 7, 1, -4, -5]))
