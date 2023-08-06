from DSAs.sorting.util import swap, key_and_reverse, get_gaps


@key_and_reverse()
def shellsort(arr, gaps=None, shrink_factor=2.2):
    """Shell sort. Stable. In place. O(N^2) time (varies). O(1) space besides gaps.

    A generalization of insertion sort where the swaps are decreasing gap sizes apart.
    The optional argument gaps should be a decreasing list of ints ending with 1.
    By default gaps is [N//k^1, N//k^2, N//k^3, ..., 1] where k is shrink_factor.
    The true time complexity depends on gaps. See wiki: wikipedia.org/wiki/Shellsort
    """
    if gaps is None:
        gaps = get_gaps(len(arr), shrink_factor)
    for gap in gaps:
        for i in range(gap, len(arr)):
            while i >= gap and arr[i] < arr[i - gap]:
                swap(arr, i, i - gap)
                i -= gap
