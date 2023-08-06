# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import numpy as np


def compress(array):
    """ Compress 3D array (i.e. trim leading/trailing and inner zeros) along first axis

    Parameters
    ----------
    array

    Returns
    -------

    """
    if array.ndim != 3:
        return np.expand_dims(array, axis=0)

    output = np.flip(np.sort(array, axis=0), axis=0)
    output = output[output.any(axis=(1, 2)), :, :]

    return output
