from DSAs.sorting.util import swap, key_and_reverse


def heapify(arr, size, i):
    largest = i
    left = 2 * i + 1
    right = left + 1

    if left < size and arr[left] > arr[largest]:
        largest = left
    if right < size and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        swap(arr, i, largest)
        heapify(arr, size, largest)


@key_and_reverse()
def heapsort(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)

    for i in range(len(arr) - 1, 0, -1):
        swap(arr, i, 0)
        heapify(arr, i, 0)
