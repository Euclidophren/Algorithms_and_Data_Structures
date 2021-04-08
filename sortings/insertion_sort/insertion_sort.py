def insertion_sort(array: list) -> list:
    n = len(array)
    for i in range(1, n):
        j = i - 1
        while j >= 0 and array[j] > array[j + 1]:
            array[j], array[j + 1] = array[j + 1], array[j]
            j -= 1
    return array


if __name__ == '__main__':
    print(insertion_sort([3, 4, 5, 7, 7, 1, -4, -5]))
