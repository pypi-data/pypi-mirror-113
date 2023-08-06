def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def getkey(key):
    if key is None:
        return lambda x: x
    return key
6