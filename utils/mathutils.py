# -*- coding: utf-8 -*-
"""
@author: rajan
"""
import math
import numpy as np
import pandas as pd

def gaussian(x, s, mu, sigma):
    """
    Adapted from MATLAB's curve-fitting tool
    Returns a Gaussian curve given x and params

    Parameters
    ---
    s: float
        scaling factor
    mu: float 
        mean of Gaussian
    sigma: float
        standard deviation of Gaussian
    
    Returns
    ---
    y-axis values of Gaussian curve 
    """
    return s * np.exp(-np.power(((x - mu)/ sigma), 2.)) 
                #/ sigma * np.sqrt(2 * np.pi)

def entropy(col, base=2):
    """
    Returns Shannon entropy of values in a pandas Series
    object, calculated using log(., base)

    Parameters
    ---
    col: pandas Series
        Series of values to calculate entropy of
    base: float
        Base of logarithm to use for entropy calculation

    Returns
    ---
    Shannon entropy as float
    """
    values = col.value_counts(normalize=True)
    return -sum([v * math.log(v, base) for v in values])