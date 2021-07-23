# -*- coding: utf-8 -*-
"""
@author: rajan
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample
from sklearn.metrics import confusion_matrix as sk_confusion_matrix

def stack_tables(dat, tab_list, ind_increment = 0):
    """
    Stacks tables of data
    """
    stack         = pd.concat([dat[t] for t in tab_list])
    stack.columns = (np.arange(dat[list(dat.keys())[0]].shape[1]) + ind_increment).astype(str)
    classes       = []
    for t in tab_list:
        classes = classes + ([t]*len(dat[t]))
    stack['class label'] = classes
    return stack


def encode_labels(stack):
    """
    Returns X data matrix, y label vector and label dictionary from stack
    """
    X          = stack.iloc[:, :-1].to_numpy()
    #make dict of labels
    classes    = stack['class label'].to_numpy()
    classlist  = stack['class label'].unique()
    label_dict = {}
    for c in enumerate(classlist):
        label_dict[c[0]+1]  = c[1]
    #make y vector
    enc           = LabelEncoder()
    label_encoder = enc.fit(classes)
    y             = label_encoder.transform(classes) + 1
    return [X, y, label_dict]


def resample_cols(X, n=None):
    """
    Resamples columns with replacement

    :param int n: number of resampled columns to return
    :return: matrix with resampled columns
    """
    if n == None:
        n = X.shape[1]
    resample_i = np.floor(np.random.rand(n) * X.shape[1]).astype(int)
    X_resample = X[:, resample_i]
    return X_resample
    

def bootstrap_auc(y, x, nboot=1000, randseed=None, switch_pos=False):
    """
    AUC of ROC curve obtained using bootstrap-resampled data

    :param int nboot: number of bootstrap resamples to  run
    :param int randseed: random seed or np.random.seed object
    :param bool switch_pos: specifies whether to flip the positive class definition 
    """
    if switch_pos:
        y = - y + max(y)
    auc_vals = []
    if x.ndim != 1:
        x = x[:,0].real
    for i in range(nboot):
        y_sample, x_sample = resample(y, x, replace=True, random_state=randseed)
        if len(np.unique(y_sample)) < 2: #both classes must be present in the sample
            continue
        auc_vals.append(roc_auc_score(y_sample, x_sample))
    auc_vals.sort()
    return [np.mean(auc_vals), auc_vals[int(0.025*len(auc_vals))], auc_vals[int(0.975*len(auc_vals))]]


def conf_matrix(y_test, y_predict):
    """
    Returns confusion matrix, given real and predicted y-vectors
    """
    # Create the raw confusion matrix
    conf = sk_confusion_matrix(y_test, y_predict)

    # Format the confusion matrix nicely
    conf = pd.DataFrame(data=conf)
    conf.columns.name = 'Predicted label'
    conf.index.name = 'Actual label'

    # Return the confusion matrix
    return conf