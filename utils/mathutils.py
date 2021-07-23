# -*- coding: utf-8 -*-
"""
@author: rajan
"""

def gaussian(x, s, mu, sigma):
    """
    Adapted from MATLAB's curve-fitting tool
    Returns a Gaussian curve given x and params

    :param float s: scaling factor
    :param float mu: mean of Gaussian
    :sigma float sigma: standard deviation of Gaussian
    :return: y-axis values of Gaussian curve 
    """
    return s * np.exp(-np.power(((x - mu)/ sigma), 2.)) #/ sigma * np.sqrt(2 * np.pi)