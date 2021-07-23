# -*- coding: utf-8 -*-
"""
@author: rajan
"""

import pandas as pd
import sys

def iter_bash(command, parameter_list):
    """
    """
    # Get number of repetitions
    iter_lens = set([len(s) for s in parameter_list])
    # assert len(iter_lens) > 1, "Parameter lists have unequal lengths"

    # Construct combined series
    script = pd.Series(command).repeat(list(iter_lens)).reset_index(drop=True)
    for pars in parameter_list:
        script += ' ' + pars

    return script

def print_to_file(script, filename):
    """
    Prints contents of pd Series to file
    """
    with open(filename, 'w') as f:
        for line in script:
            print(line, file=f)

def unixify(script):
    """
    """
    pattern = r'(?P<drive_letter>([A-Z]:))'
    rep = lambda m: '/mnt/' + m.group('drive_letter').lower()
    return script.str.replace(pattern, rep, regex=True).str.replace(':','').str.replace('\\', '/')