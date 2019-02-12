# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:44:52 2019

@author: Yu
"""

import os
import numpy as np
from glob import glob
import pandas as pd
from collections import defaultdict


def plate_sample_techfile(plate_id, plate_map, echem_tech):
    '''
    input: plate_id (number 4 digit), plate_map (number 2 digit), echem_tech (string, e.g. CV2)
    output: a dictionary which is able to trace the echem techfile of specified sample number from a specified plate
    '''
    
    plate_map_file_path = glob(r"J:\hte_jcap_app_proto\map\00{}*mp.txt".format(plate_map))[0]
    plate_map = pd.read_csv(plate_map_file_path, header=1)
    plate_map.set_index('% Sample', inplace=True) # set sample number as indexes
    unique_sample_numbers = plate_map.index.values 
    
    #grab all techfiles in the sub_folders
    plate_folder_path = glob("C:\INST\RUNS\*{}*".format(str(plate_id)))[0]
    techfile_paths = glob(os.path.join(plate_folder_path, '*\*{}.txt*'.format(echem_tech))) 
    
    # {sample number : [techfile_paths (could be more than one)]} 
    sample_techfile_dict = defaultdict(list)
    for unique_sample_number in unique_sample_numbers:
        for techfile_path in techfile_paths:
            sample_number = int(os.path.basename(techfile_path).split('_')[0].strip('Sample'))
            if sample_number==unique_sample_number:
                sample_techfile_dict[unique_sample_number].append(techfile_path) 

    # select only the most recent techfiles per each unique sample number
    for sample_number, techfile_list in sample_techfile_dict.items():
        if len(techfile_list) > 1:
            sample_ctimes = [os.path.getctime(techfile) for techfile in techfile_list]
            max_index = np.array(sample_ctimes).argmax() # index of the maxmium ctime, i.e. most recent one
            desired_techfile = techfile_list[max_index]
            del techfile_list[:]
            techfile_list.append(desired_techfile)
    
    # final {sample number : techfile_path} 
    final_sample_techfile_dict = {}
    for sample_number, techfile_list in sample_techfile_dict.items():
        final_sample_techfile_dict[sample_number] = techfile_list[0]
    
    return final_sample_techfile_dict