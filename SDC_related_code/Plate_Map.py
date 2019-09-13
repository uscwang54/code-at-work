# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:15:21 2019

@author: Yu Wang
"""

import pandas as pd
from glob import glob

def plate_map_dict(plate_map):
    '''
    input: plate_map (2 digit)
    output: sample_location_dict = {(x,y):sample_number}
    '''
    
    plate_map_file_path = glob(r"J:\hte_jcap_app_proto\map\00{}*mp.txt".format(plate_map))[0]
    plate_map = pd.read_csv(plate_map_file_path, header=1)
    sample_number = plate_map['% Sample']
    sample_x = plate_map[' x(mm)']
    sample_y = plate_map[' y(mm)']
    A_frac = plate_map[' A(fraction)']
    B_frac = plate_map[' B(fraction)']
    C_frac = plate_map[' C(fraction)']
    D_frac = plate_map[' D(fraction)']
    E_frac = plate_map[' E(fraction)']
    F_frac = plate_map[' F(fraction)']
    
    sample_loc_dict = {sample_num:(sample_x[i],sample_y[i]) for i, sample_num in enumerate(sample_number)}
    sample_comp_dict = {sample_num:(A_frac[i],B_frac[i],C_frac[i],D_frac[i],E_frac[i],F_frac[i]) for i, sample_num in enumerate(sample_number)}
    
    return sample_loc_dict,sample_comp_dict
    