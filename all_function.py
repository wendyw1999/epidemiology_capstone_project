import pandas as pd
import os
import shutil
import shlex
import sys
import subprocess as sp
import time
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.pyplot as plot
import re
import json
import time
import gzip
import requests
def download_data(target, datapath): # url could be got based on target
    """
    Copies/Downloads target csv file to the local data directory
    every url is from data_param.json
    """
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    r = requests.get(url, allow_redirects=True)
    open(datapath+target, 'wb').write(r.content)


def download(datapath, recovered, death, confirmed, mobility):
    """
    download all data we need here 
    datapath = /data # path to all files
    recovered = path to download
    death = path to download
    confirmed = path to download
    mobility  = path to download
    """
    t1 = time.time()
    download_data(datapath, recovered)
    t2 = time.time()
    print("recovered files done. Time: {0:.0f} s".format(t2 - t1))
    print("Downloading Death cases files...")
    download_data(datapath, death)
    t1 = time.time()
    print("Death cases files done. Time: {0:.0f} s".format(t1 - t2))
    print("Downloading confirmed files...")
    download_data(datapath, confirmed)
    t2 = time.time()
    print("confirmed cases files done. Time: {0:.0f} s".format(t2 - t1))
    print("Downloading mobility files...")
    download_data(datapath, mobility)
    t1 = time.time()
    print("mobility files done. Time: {0:.0f} s".format(t1 - t2))
    print('All finished')
    
def processing():
    '''
    execute stimulations 
    run the model
    ? maybe some interactive? not now
    '''
    return 
def visualization():
    '''
    plot based on the modules
    pyplot/sns
    '''
    return 