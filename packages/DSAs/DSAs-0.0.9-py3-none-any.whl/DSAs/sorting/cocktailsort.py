
from DSAs.sorting.util import swap, key_and_reverse


@key_and_reverse()
def cocktailsort(arr):
    """Cocktail sort - bidirectional bubble sort. Stable. In place. O(N^2) time. O(1) extra space."""
    left, right = 0, len(arr) - 1
    while left < right:
        for i in range(left, right):
            if arr[i] > arr[i + 1]:
                swap(arr, i, i + 1)
        right -= 1
        for i in range(right, left, -1):
            if arr[i] < arr[i - 1]:
                swap(arr, i, i - 1)
        left += 1
