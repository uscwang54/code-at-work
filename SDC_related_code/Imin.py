# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:48:24 2019

@author: Yu Wang
"""

from __future__ import division
import sys
sys.path.append(r"C:\Users\eche\Desktop\IPYNB\Utility") #append the utility folder path
import os
import re
import numpy as np
import pandas as pd
from collections import defaultdict,OrderedDict
import matplotlib.pyplot as plt
import operator
from Plate_Sample_File import plate_sample_techfile
from Quality_Check import CV2_quality_check
from Plate_Map import plate_map_dict

# plot the plate map with each sample represented by a square dot
# the color of the dot represents the minimum current during the CV scan, i.e. max current

###################################################################################
parent_folder_path = r"C:\INST\RUNS\20190603_MnNiMgCaFeY-postPETS_50522" #needs to be updated
###################################################################################

plate_id = int(os.path.basename(parent_folder_path).split("_")[-1][:-1])
plate_map = 69 #needs to be updated if necessary
echem_tech = 'CV2' #needs to be updated if necessary
scan_type = 'post' if 'post' in parent_folder_path else 'pre'

sample_techfile_dict = plate_sample_techfile(plate_id, plate_map, echem_tech, scan_type)
sample_loc_dict,sample_comp_dict = plate_map_dict(plate_map)

I = defaultdict(np.ndarray) # I = {sample number : array(I(A))}
for sample_number, CV2_file_path in sample_techfile_dict.items():    
    #if CV2_quality_check(CV2_file_path): # check if sample scan passes cv2 quality check
    with open(CV2_file_path) as f:
        txt = f.readlines()    
        current = np.zeros(shape=(len(txt[15:])))  
        for index,line in enumerate(txt[15:]):
            current[index] = float(line.split()[-2])
    I[sample_number] = current
    
Imin = {sample_number:np.min(current) for sample_number, current in I.items()} # Imin = {sample number: Imin(A)}

X = [sample_loc_dict[sample_number][0] for sample_number in Imin]
Y = [sample_loc_dict[sample_number][1] for sample_number in Imin]

plt.figure(figsize=(16,10))
plt.title('plate{}_{}PETS: I_min (A)'.format(plate_id, scan_type))
sc = plt.scatter(X, Y, c=Imin.values(), s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='I_min (A)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    
    
sorted_Imin = sorted(Imin.items(), key=operator.itemgetter(1))
top10_sample = [sample_number for sample_number, i_min in sorted_Imin][:10]
top10_sample_comp = [sample_comp_dict[sample] for sample in top10_sample]
top10_sample_dict = OrderedDict(zip(top10_sample, top10_sample_comp))
elements = re.findall('[A-Z][^A-Z]*', os.path.basename(parent_folder_path).split('_')[1].rstrip('-postPETS'))
top10_sample_df = pd.DataFrame.from_dict(top10_sample_dict, orient='index')
top10_sample_df.columns = elements
    
print top10_sample_df #top 10 of best performers
