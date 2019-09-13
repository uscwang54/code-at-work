# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:49:38 2019

@author: Yu Wang
"""

from __future__ import division
import sys
sys.path.append(r"C:\Users\eche\Desktop\IPYNB\Utility") #append the utility folder path
import re
import os
import numpy as np
import pandas as pd
from glob import glob
from collections import defaultdict,OrderedDict
import matplotlib.pyplot as plt
import operator
from scipy.signal import find_peaks_cwt
from Plate_Sample_File import plate_sample_techfile
from Quality_Check import CV2_quality_check
from Plate_Map import plate_map_dict

###################################################################################
parent_folder_path = r"C:\INST\RUNS\20190528_MnNiMgCaFeY_50522" #needs to be updated
###################################################################################

plate_id = int(os.path.basename(parent_folder_path).split("_")[-1][:-1])
plate_map = 69 #needs to be updated if necessary
echem_tech = 'CV2' #needs to be updated if necessary
scan_type = 'post' if 'post' in parent_folder_path else 'pre'

sample_techfile_dict = plate_sample_techfile(plate_id, plate_map, echem_tech, scan_type)
sample_loc_dict,sample_comp_dict = plate_map_dict(plate_map)

rcp = glob(os.path.join(parent_folder_path,"*\*.rcp"))[0]
with open(rcp) as f:
    txt = f.readlines()
    for i,line in enumerate(txt):
        if re.search(r'echem_params__CV2:',line):
            CV2_start_index = i
    CV2_params_txt = txt[CV2_start_index:CV2_start_index+14] #there are 14 lines of params within CV2 block
    for line in CV2_params_txt:     
        if re.search(r"final_potential_vref:",line):
            E_final = float(line.split()[-1])
        if re.search(r'num_potential_cycles:',line):
            num_cycle = int(line.split()[-1])
            
E_onsite = {} # E_onsite = {sample number : onsite_potential}
for sample_number, CV2_file_path in sample_techfile_dict.items():   
    with open(CV2_file_path) as f:
        txt = f.readlines()    
        data = np.zeros(shape=(len(txt[15:]),3))  
        for index,line in enumerate(txt[15:]):
            data[index,0] = float(line.split()[0]) #t(s)
            data[index,1] = float(line.split()[1]) #Ewe(V)
            data[index,2] = float(line.split()[-2]) #I(A)    
    #ind = [i for i, E in enumerate(Ewe) if np.isclose(E,E_final,rtol=2e-04, atol=6e-06)]
    peak_ind = find_peaks_cwt(data[:,1], np.arange(1,1000))
    try:
        assert len(peak_ind)==num_cycle+1
    except AssertionError:
        print sample_number
    mydata = data[peak_ind[-2]:peak_ind[-1],:] #the last CV cycle
    key_ind = find_peaks_cwt(mydata[:,1], np.arange(1,1000))
    assert len(key_ind)==3 #the last cv cycle has start, turn-around, end point
    
    start_ind = key_ind[0]
    turn_around_ind = key_ind[1]
    cathodic_data = mydata[start_ind:turn_around_ind,:]
   
    onsite_potentials = [cathodic_data[index,1] for index,current in enumerate(cathodic_data[:,2]) if np.isclose(current,0.,rtol=1e-05, atol=5e-08)]
    onsite_potential = np.mean(onsite_potentials)
    E_onsite[sample_number] = onsite_potential
            
X = [sample_loc_dict[sample_number][0] for sample_number in E_onsite]
Y = [sample_loc_dict[sample_number][1] for sample_number in E_onsite]

plt.figure(figsize=(16,10))
plt.title('plate{}_{}PETS: onsite_potential (V)'.format(plate_id, scan_type))
sc = plt.scatter(X, Y, c=E_onsite.values(), s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='onsite_potential (V)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    