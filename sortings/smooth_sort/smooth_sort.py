import heapq


def leonardo_numbers(size: int) -> list:
    numbers = [1, 1]
    next_number = numbers[-1] + numbers[-2] + 1
    while len(numbers) >= 2 and size > next_number:
        numbers.append(next_number)
        next_number = numbers[-1] + numbers[-2] + 1
    numbers.reverse()
    return numbers


def do_list_heaps(data):
    leonardo_nums = leonardo_numbers(len(data))
    list_heaps = []
    m = 0 
    for i in leonardo_nums:
        if len(data) - m >= i:
            list_heaps.append(data[m : m+i])
            m += i
    for i in list_heaps:
        heapq.heapify(i)
    list_heaps.reverse()
    return list_heaps


def count_indices(i, indices):
    indices.append(2 * indices[i] + 1)
    indices.append(2 * indices[i] + 2)
    return indices


def get_list(index_part, heap):
    heap_part = []
    for i in index_part:
        if i < len(heap):
            heap_part.append(heap[i])
    return heap_part


def heap_division(heap):
    index = 0
    indices_left, indices_right = [1], [2]
    while indices_left[-1] < len(heap): 
        indices_left = count_indices(index, indices_left)
        indices_right = count_indices(index, indices_right)
        index += 1
    heap_left = get_list(indices_left, heap)
    heap_right = get_list(indices_right, heap)
    return heap_left, heap_right


def smooth_sort(list_heaps):
    heap_left, heap_right = [], []
    result = []
    while list_heaps:
        flag = 0
        min_index = list_heaps.index(min(list_heaps))
        current_root = list_heaps[0][0]
        current_min = list_heaps[min_index][0]
        heapq.heapreplace(list_heaps[0], current_min)
        heapq.heapreplace(list_heaps[min_index], current_root)
        if len(list_heaps[0]) > 1:
            heap_left, heap_right = heap_division(list_heaps[0])
            flag = 1
        minimum = heapq.heappop(list_heaps[0])
        result.append(minimum)
        list_heaps.pop(0)
        if flag == 1:
            list_heaps.insert(0, heap_left)
            list_heaps.insert(0, heap_right)
    return result


if __name__ == '__main__':
    print(smooth_sort([3, 4, 5, 7, 7, 1, -4, -5]))
