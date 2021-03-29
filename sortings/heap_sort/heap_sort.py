def heap_sort(array: list) -> list:
    heapify(array, len(array))
    end = len(array) - 1
    while end > 0:
        array[end], array[0] = array[0], array[end]
        end -= 1
        sift_down(array, 0, end)
    return array


def heapify(array: list, count: int):
    start = int((count - 2) / 2)
    while start >= 0:
        sift_down(array, start, count - 1)
        start -= 1


def sift_down(array: list, start: int, end: int):
    root = start
    while (root * 2 + 1) <= end:
        child = root * 2 + 1
        swap = root
        if array[swap] < array[child]:
            swap = child
        if (child + 1) <= end and array[swap] < array[child + 1]:
            swap = child + 1
        if swap != root:
            array[root], array[swap] = array[swap], array[root]
            root = swap
        else:
            return


if __name__ == '__main__':
    print(heap_sort([3, 4, 5, 7, 7, 1, -4, -5]))
