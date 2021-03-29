from math import floor


def bubble_sort(array: list) -> list:
    size = len(array) - 1
    for i in range(size):
        for j in range(size - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def bubble_sort_optimized(array: list) -> list:
    size, i = len(array) - 1, 0
    t = True
    while t:
        t = False
        for j in range(size - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                t = True
        i += 1
    return array


def odd_even_sort(array: list) -> list:
    size = len(array)
    for i in range(size):
        if i % 2:
            for j in range(1, size, 2):
                if array[j] < array[j - 1]:
                    array[j - 1], array[j] = array[j], array[j - 1]
        else:
            for j in range(2, size, 2):
                if array[j] < array[j - 1]:
                    array[j - 1], array[j] = array[j], array[j - 1]
    return array


def get_gap(gap):
    gap = floor((gap * 10) / 13)
    return 1 if gap < 1 else gap


def comb_sort(array: list) -> list:
    gap, size = len(array), len(array)
    swapped = True
    while gap != 1 or swapped:
        gap = get_gap(gap)
        swapped = False
        for i in range(size - gap):
            if array[i + gap] < array[i]:
                array[i], array[i + gap] = array[i + gap], array[i]
                swapped = True
    return array


def shaker_sort(array: list) -> list:
    begin, end = 0, len(array) - 2
    swapped = True
    while swapped:
        swapped = False
        for i in range(begin, end + 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end, begin - 1, -1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        begin += 1
    return array
