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
