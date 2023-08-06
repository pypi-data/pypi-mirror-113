from DSAs.sorting.util import swap, key_and_reverse


@key_and_reverse()
def selectionsort(arr):
    """Selection sort. Unstable. In place. O(N^2) time. O(1) extra space."""
    for i in range(len(arr)):
        min_index = i + min(range(len(arr) - i), key=arr[i:].__getitem__)
        swap(arr, i, min_index)
