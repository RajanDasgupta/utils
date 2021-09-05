from scipy.io import loadmat
import pandas as pd
import easygui
import pickle
import os

def import_mat (filename = ''):
    data = []
    if len(filename) == 0:
        filename = easygui.fileopenbox(msg='Select a .mat file')
    try:
        matfile = loadmat(filename)
        data    = matfile['dat']
    finally:
        return data

def load_dat (data, return_list=False):
    if return_list:
        dat = [pd.DataFrame(item) for item in data[0][0]]
        return dat
    else:
        dat     = {}
        keys    = [item[0] for item in data[0][0].dtype.descr]
        for count, item in enumerate(data[0][0]):
            dat[keys[count]] = pd.DataFrame(item)
        return dat

def load_multi (return_list=False, auto=False):
    if auto:
        dat_dir  = easygui.diropenbox(msg='Choose data directory')
        files    = [dat_dir+'\\'+s for s in os.listdir(dat_dir)]
        dat_list = [load_dat(import_mat(filename=f)) for f in files]
    else:
        cont = True
        while cont:
            data = import_mat()
            dat_list.append(load_dat(data, return_list=return_list))
            cont = easygui.ynbox(msg='Select another file?')
    return dat_list

def concat_dat (dat_list):
    dat = dat_list[0]
    for item in dat_list[1:]:
        new_dat = {}
        for key in item:
            new_dat[key] = pd.concat([dat[key], item[key]], axis=1)
        dat = new_dat
    return dat

def save_dat(data):
    filename  = easygui.filesavebox(msg='Save file')
    filename += '.pickle'
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        
def get_data():
    filename = easygui.fileopenbox()
    dat      = pickle.load(open(filename, "rb" ))
    return dat