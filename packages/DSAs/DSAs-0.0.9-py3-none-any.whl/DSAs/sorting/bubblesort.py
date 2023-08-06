from DSAs.sorting.util import swap, key_and_reverse


@key_and_reverse()
def bubblesort(arr):
    """Bubble sort. In place. Stable. O(N^2) time. O(1) extra space."""
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)
