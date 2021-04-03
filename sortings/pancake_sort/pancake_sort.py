def pancake_sort(array: list) -> list:
    curr_size = len(array)
    while curr_size > 1:
        mi = find_max(array, curr_size)
        if mi != curr_size - 1:
            flip(array, mi)
            flip(array, curr_size - 1)
        curr_size -= 1
    return array


def flip(array: list, n: int):
    start = 0
    while start < n:
        tmp = array[start]
        array[start] = array[n]
        array[n] = tmp
        start += 1
        n -= 1


def find_max(array: list, n: int):
    mi = 0
    for i in range(0, n):
        if array[i] > array[mi]:
            mi = i
    return mi


if __name__ == '__main__':
    print(pancake_sort([3, 4, 5, 7, 7, 1, -4, -5]))
