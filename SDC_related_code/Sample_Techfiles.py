#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import re
import numpy as np
from glob import glob
import pandas as pd
from collections import defaultdict

def sample_techfiles_from_plate(plate_id):
    '''
    given plate_id, return a dictionary with sample_number:[list of techfiles] pairs.
    
    input: plate_id (int: 4 digit).
    output: a dictionary with sample_number:[list of techfiles] pairs.
    '''
    # get the parent folder path for the plate
    run_folders = os.listdir(r'C:\INST\RUNS') 
    for folder in run_folders:
        if str(plate_id)==folder.split('_')[-1][:4]:
            parent_folder = os.path.join('C:\INST\RUNS', folder)

    # go inside the .done or .copied subfolders to collect all the sample_id:[list of techfiles] pairs
    all_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            all_files.append(os.path.join(root, file))

    # create sample_id:[asociated techfiles] dictionary
    sample_techfiles = defaultdict(list)
    for file in all_files:
        if "Sample" in file:
            sample_id = int(os.path.basename(file).split('_')[0].strip("Sample"))
            sample_techfiles[sample_id].append(file)

    # check if there are samples got rescanned (should not be a problem if not allowed)

    # grab the rcp and count the number of echem_params
    rcp = [file for file in all_files if 'rcp' in file][0]
    with open(rcp) as f:
        echem_params = []
        for line in f:
            res = re.search(r'echem_params__([A-Z]{2,}\d+)', line)
            if res:
                echem_params.append(res.group(1))
            else:
                continue
    num_echem_params = len(echem_params)

    # check if every sample_id has the correct number of techfiles. If not, choose the most recent ones
    for sample_id, techfiles in sample_techfiles.items():
        if len(techfiles)==num_echem_params:
            continue
        else:
            techfiles = techfiles[-num_echem_params:] # the most recent techfiles 
    
    return sample_techfiles

