#!/usr/bin/env python

import numpy as np

__author__ = "Sebastian Kiehlmann"
__credits__ = ["Sebastian Kiehlmann"]
__license__ = "BSD 3"
__version__ = "1.0"
__maintainer__ = "Sebastian Kiehlmann"
__email__ = "skiehlmann@mail.de"
__status__ = "Production"

#==============================================================================
# FUNCTIONS
#==============================================================================

def smart_binning(time, interval, verbose=0):
    """Find data binning intervals.

    Iteratively finds ranges of time-sorted data, where the data falls into a
    defined time interval. This function provides an alternative to regular
    binning of data with uneven time sampling.

    Parmeters
    ---------
    time : array-like
        Sorted time marks.
    interval : float
        The length of the interval, in which data points are considered to be
        close to one another.
    verbose : int, optional
        If zero, no information is printed. Otherwise, information about the
        identified intervals is printed. The default is 0.

    Raises
    ------
    ValueError
        Raised if `time` is not sorted increasingly.

    Returns
    -------
    out : list
        A list of arrays containing indices to the data points which are in the
        same bin.
    """

    time = np.asarray(time)

    # check that time is sorted increasingly:
    if np.any(np.diff(time) < 0):
        raise ValueError("The provided time are not sorted increasingly.")

    if len(time) < 2:
        return []

    # first, find all intervals:
    intervals = []

    # iterate through time values:
    for i, value in enumerate(time):
        # iterate backwards throuch preceding values:
        j = i-1

        while j>=0 and time[j] > value - interval:
            j -= 1
        else:
            # replace latest interval with extended interval:
            if j+1 < i and len(intervals)>0 and intervals[-1][0] == j+1:
                intervals[-1] = [j+1, i+1]
            # add new interval:
            elif j+1 < i:
                intervals.append([j+1, i+1])

    if len(intervals) == 0:
        return False

    # second, find best interval:
    spreading = []

    for inter in intervals:
        spreading.append(np. std(time[inter[0]:inter[1]]))

    index = spreading.index(min(spreading))
    bin_ids_cur = np.arange(intervals[index][0], intervals[index][1])

    # third, recursion on preceeding time:
    time_pre = time[:bin_ids_cur[0]]
    bin_ids_pre = smart_binning(time_pre, interval)

    # fourth, recursion on succeeding time:
    time_suc = time[bin_ids_cur[-1]+1:]
    bin_ids_suc = smart_binning(time_suc, interval)

    # fifth, join indices lists:
    if bin_ids_pre:
        bin_ids = bin_ids_pre
        bin_ids.append(bin_ids_cur)
    else:
        bin_ids = [bin_ids_cur]

    if bin_ids_suc:
        # adjust indices:
        add = bin_ids_cur[-1]+1
        for inter in bin_ids_suc:
            bin_ids.append(inter +add)

    # print information:
    if verbose:
        n = [len(ids) for ids in bin_ids]
        print(f'{len(bin_ids)} bins found.')
        print('time points per bin:')
        print(f'  Min:    {np.min(n):8d}')
        print(f'  Median: {np.median(n):8.0f}')
        print(f'  Mean:   {np.mean(n):8.0f}')
        print(f'  Max:    {np.max(n):8d}')

    return bin_ids

#==============================================================================

def split_data(time, gap):
    """Split a time series at large gaps.

    Parameters
    ----------
    time : array-like
        Sorted time marks.
    gap : float
        Gap length threshold. The data is split when the time interval between
        data points exceeds this value.

    Returns
    -------
    out : list
        List of arrays containing indices to the split data sets.
    """

    time = np.asarray(time)

    # check that time is sorted increasingly:
    if np.any(np.diff(time) < 0):
        raise ValueError("The provided time are not sorted increasingly.")

    if len(time) < 2:
        return []

    # identify large gaps:
    split = np.r_[0, np.nonzero(np.diff(data)>gap)[0] + 1, len(data)]
    indices = []

    # prepare list of indices to the split data sets:
    for start, stop in zip(split[:-1], split[1:]):
        indices.append(np.arange(start, stop))

    return indices

#==============================================================================
