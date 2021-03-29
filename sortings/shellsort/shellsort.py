from math import floor


def shell_sort(array: list):
    inc = len(array) // 2
    while inc:
        for i, el in enumerate(array):
            while i >= inc and array[i - inc] > el:
                array[i] = array[i - inc]
                i -= inc
            array[i] = el
        inc = 1 if inc == 2 else floor(inc * 5.0 / 11)
    return array


if __name__ == '__main__':
    print(shell_sort([3, 4, 5, 7, 7, 1, -4, -5]))
