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

def mask_outliers(x, window_length, threshold):
    """Identify outliers.

    Parameters
    ----------
    x : array-like
        Time-sorted data sequence.
    window_length : int
        Defines the width of the Hann window function that is used to calculate
        a smoothed data curve.
    threshold : float
        Threshold for detecting outliers. Residuals that are larger than the
        mean residual value times this threshold factor are considered
        outliers.

    Raises
    ------
    ValueError
        Raised, if `window_length` is not an integer.

    Returns
    -------
    outlier : np.ndarray (dtype: bool)
        Items are True if a value in the input `x` is considered an outliers;
        False otherwise.
    """

    # check input:
    x = np.asarray(x)

    if not isinstance(window_length, int):
        raise ValueError("`window_length` must be integer.")

    # smoothed data:
    s = np.r_[x[window_length-1:0:-1], x, x[-2:-window_length-1:-1]]
    w = np.hanning(window_length)
    n = int(np.floor(window_length/2))
    x_smoothed = np.convolve(w/w.sum(), s, mode='valid')[n:-n]

    # residuals:
    x_res = np.absolute(x - x_smoothed)
    mean_res = x_res.mean()

    # identify outliers:
    outlier = x_res > threshold * mean_res

    return outlier

#==============================================================================

def mask_largeunc(x_unc, threshold):
    """Identify large uncertainties.

    Parameters
    ----------
    x_unc : array-like
        Data uncertainties.
    threshold : float
        Threshold for detecting large uncertainties. Uncertainties that are
        larger than the mean uncertainty times this threshold factor are
        considered large.

    Returns
    -------
    large_unc : np.ndarray (dtype: bool)
        Items are True if a value in the input `x_unc` is considered a large
        uncertainty; False otherwise.
    """

    x_unc = np.asarray(x_unc)

    mean_unc = x_unc.mean()
    large_unc = x_unc > threshold * mean_unc

    return large_unc

#==============================================================================
