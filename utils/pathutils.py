# -*- coding: utf-8 -*-
"""
@author: rajan
"""

import os
import easygui
import numpy as np
import pandas as pd
from pathlib import Path

def get_directory():
    """
    Opens prompt to select directory
    """
    return easygui.diropenbox()

def folder_list(directory):
    """
    Returns list of absolute paths of sub-directories
    """
    this_dir = [os.path.join(directory, name) for name in os.listdir(directory)]
    return [name for name in this_dir if os.path.isdir(name)]

def file_list(directory):
    """
    Returns absolute paths of files in directory as a list
    """
    this_dir = [os.path.join(directory, name) for name in os.listdir(directory)]
    return [name for name in this_dir if not os.path.isdir(name)]

def file_series(directory, ext='*', recursive=False):
    """
    Returns Pandas Series of lists containing split versions of absolute paths 
    of files in directory    
    """
    files = directory.glob('**/*.' + ext) if recursive else directory.glob('*.' + ext)
    return pd.Series([f.__str__() for f in files], dtype=str).str.split('\\')

def random_files(n=5, d=None):
    """
    Returns list of randomly selected files in directory
    """
    if d is None:
        d = get_directory()
        if d is None:
            return
    files = file_list(d)
    
    # Return all files if not enough files in dir
    if n >= len(files):
        return files
    file_inds = [0, 0] 
    
    # Generate random indices without repetitions
    while len(np.unique(file_inds)) != n:
        file_inds = [round(ind) for ind in np.random.rand(n) * len(files)]
    return [files[ind] for ind in file_inds]

def random_files_recursive(n=5, d=None):
    """
    Returns list of randomly selected files from current directory and subdirectories
    """
    if d is None:
        d = get_directory()
        if d is None:
            return
    files = random_files(n, d)
    dirs = folder_list(d)
    
    # For each subdirectory, call function recursively
    for folder in dirs:
        files += random_files_recursive(n, folder)
    return files

def changed_filenames(from_r, to_r, d=None, ext='*', recursive=False):
    """
    :param str from_r: string or pattern to replace. can be regEx pattern with multiple 
                        named capture groups

    :param str to_r: string to replace with OR function specifying which capture group 
                        to return and how, for instance lambda m: m.group('two')
    """
    # Get directory if empty
    if d is None:
        d = Path(get_directory())
        if d is None:
            return

    # Get list of files
    file_list = file_series(d, ext=ext, recursive=recursive)
    
    # Process filenames
    if len(file_list) != 0:
        # Find indexes of files with capture group
        filenames = file_list.apply(lambda l: l[-1])
        matches = filenames.str.contains(from_r)
        # Replace string/capture groups in relevant rows
        newnames = filenames[matches].str.replace(from_r, to_r, regex=True)
        # Construct full paths and return
        paths = file_list[matches].apply(lambda l: l[:-1]).str.join('\\')
        new_names = paths + '\\' + newnames
        old_names = paths + '\\' + filenames[matches]
        return old_names.reset_index(drop=True), new_names.reset_index(drop=True)
    else:
        print('No files found')
