# -*- coding: utf-8 -*-
"""
@author: rajan
"""
import numpy as np
import pandas as pd



def clean_data(dat, how='mean', axis=0):
    """
    Returns function to handle numerical missing values in multiple DataFrames

    :param str how: the function to use to handle missing values.
                    Can be either:
                    nan: replace with NaNs
                    mean: replace with means. Axis can be specified, default 0
                    drop: drop rows/cols with missing values. Default axis=0
    :param int axis: axis along which to apply func
    :return: modified DataFrames
    """
    for tab in dat:
        min_val = dat[tab].min().min()
        dat[tab].replace(to_replace=min_val, value=np.nan, inplace=True)
    switcher = {
            'nan': lambda dat: dat,
            'mean': nan_to_mean,
            'drop': drop_nan_trials
            }
    func = switcher.get(how, lambda:'Invalid method')
    return func(dat, axis=axis)


def drop_nan_trials(dat, axis=0):
    """
    Drops rows/columns with missing values in each DF
    """ 
    for tab in dat:
        dat[tab].dropna(axis=axis, inplace=True)
    return dat


def nan_to_mean(dat, axis=0):
    """
    Imputes missing values as the row/column mean in each DF
    """ 
    for tab in dat:
        dat[tab] = dat[tab].apply(lambda series: series.fillna(series.mean()), axis=axis)
    return dat