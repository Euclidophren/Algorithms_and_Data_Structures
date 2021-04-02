import multiprocessing


def mergesort_parallel(lst):
    if len(lst) == 1:
        return lst
    else:
        m = int(len(lst) / 2)
        l = mergesort_parallel(lst[:m])
        r = mergesort_parallel(lst[m:])
        return par_merge(l, r, lst)


def mergesort_sequential(lst):
    if len(lst) == 1:
        return lst
    else:
        m = int(len(lst) / 2)
        l = mergesort_sequential(lst[:m])
        r = mergesort_sequential(lst[m:])
        return seq_merge(l, r, lst)


def seq_merge(l, r, lst):
    i, j, k = 0, 0, 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            lst[k] = l[i]
            i += 1
        else:
            lst[k] = r[j]
            j += 1
        k += 1

    while i < len(l):
        lst[k] = l[i]
        i += 1
        k += 1

    while j < len(r):
        lst[k] = r[j]
        j += 1
        k += 1
    return lst


def par_merge(l, r, lst):
    for i in range(len(l)):
        lst[i + par_bin_search(l[i], r)] = l[i]
    for i in range(len(r)):
        lst[i + par_bin_search(r[i], l)] = r[i]

    return lst


def seq_bin_search(item, alist):
    first, last = 0, len(alist) - 1
    while first <= last:
        midpoint = (first + last) // 2
        if item < alist[midpoint]:
            last = midpoint - 1
        else:
            first = midpoint + 1
    return first


def par_bin_search(el, arr):
    max_cores = multiprocessing.cpu_count()
    jobs = []
    bin_array = [0] * max_cores
    idx_array = [0] * max_cores

    if len(arr) < max_cores + 1:
        idx = seq_bin_search(el, arr)
        return idx
    else:
        processing_field = len(arr) // (max_cores + 1)
        for core in range(max_cores):
            idx_array[core] = (core + 1) * processing_field - 1

        def comparison(el, core):
            right = (idx_array[core])
            if el >= arr[right]:
                bin_array[core] = 0
            else:
                bin_array[core] = 1

        for i in range(max_cores):
            p = multiprocessing.Process(target=comparison, args=(el, i, processing_field))
            p.daemon = False
            jobs.append(p)
            p.start()
        for p in jobs:
            p.join()
        if bin_array[0] == 1:
            return par_bin_search(el, arr[:idx_array[0] + 1])
        elif bin_array[-1] == 0:
            return par_bin_search(el, arr[idx_array[-1]:])
        else:
            idx = 0
            while (idx < max_cores) and (bin_array[idx] == 0):
                idx += 1
            if idx_array[idx - 1] + 1 < idx_array[idx]:
                par_bin_search(el, arr[idx_array[idx - 1]:idx_array[idx] + 1])
            else:
                return idx_array[idx - 1]


if __name__ == '__main__':
    print(mergesort_parallel([3, 4, 1, 1, 6, 0, -4, 5, 5]))
