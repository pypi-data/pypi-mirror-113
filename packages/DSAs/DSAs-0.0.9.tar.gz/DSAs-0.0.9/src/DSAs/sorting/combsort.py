from DSAs.sorting.util import swap, key_and_reverse, get_gaps


@key_and_reverse()
def combsort(arr, gaps=None, shrink_factor=1.3):
    """Comb sort. Unstable in general. In place. O(N^2) time (varies). O(1) space besides gaps.

    A generalization of bubble sort where the swaps are decreasing gap sizes apart.
    The optional argument gaps should be a decreasing list of ints ending with 1.
    By default gaps is [N//k^1, N//k^2, N//k^3, ..., 1] where k is shrink_factor.
    The true time complexity depends on gaps.
    """
    if gaps is None:
        gaps = get_gaps(len(arr), shrink_factor)
    gap_index = 0
    done = False
    while not done:
        if gap_index < len(gaps):
            done = False
            gap = gaps[gap_index]
            gap_index += 1
        else:
            done = True
            gap = gaps[-1]
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                swap(arr, i, i + gap)
                done = False
