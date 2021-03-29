def bucket_sort(array: list, num_buckets: int) -> list:
    buckets, result = [[] for i in range(num_buckets)], []
    min_elem, max_elem, size = -10000, 10000, len(array)
    for i in range(size):
        min_elem, max_elem = min(min_elem, array[i]), max(max_elem, array[i])
    diff = max_elem - min_elem
    for i in range(size):
        index = int(array[i] * num_buckets / diff)
        buckets[index].append(array[i])
    for i in range(num_buckets):
        buckets[i].sort()
    for i in range(num_buckets):
        for k in range(len(buckets[i])):
            result.append(buckets[i][k])
    return result


def bucket_sort_recursive(array: list, num_buckets: int, min_elem, max_elem) -> list:
    buckets, result = [[] for i in range(num_buckets)], []
    min_buckets, max_buckets = [], []
    size = len(array)
    if size == 1 or min_elem == max_elem:
        return array
    else:
        diff = max_elem - min_elem
        for i in range(size):
            index = int(array[i] * num_buckets / diff)
            buckets[index].append(array[i])
            min_buckets.append(min(buckets[index], array[i]))
            max_buckets.append(max(buckets[index], array[i]))
        for i in range(num_buckets):
            bucket_sort_recursive(buckets[i], num_buckets, min_buckets[i], max_buckets[i])
        for i in range(num_buckets):
            for k in range(len(buckets[i])):
                result.append(buckets[i][k])
        return result
