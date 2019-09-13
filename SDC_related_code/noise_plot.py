# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:52:19 2019

@author: Yu Wang
"""

from __future__ import division
import sys
sys.path.append(r"C:\Users\eche\Desktop\IPYNB\Utility") #append the utility folder path
import numpy as np
import os
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from Plate_Sample_File import plate_sample_techfile
from Quality_Check import CV2_quality_check
from Plate_Map import plate_map_dict

###################################################################################
parent_folder_path = r"C:\INST\RUNS\20190603_MnNiMgCaFeY-postPETS_50522" #needs to be updated
###################################################################################

plate_id = int(os.path.basename(parent_folder_path).split("_")[-1][:-1])
plate_map = 69 #needs to be updated if necessary
echem_tech = 'CV2' #needs to be updated if necessary
scan_type = 'post' if 'post' in parent_folder_path else 'pre'

sample_techfile_dict = plate_sample_techfile(plate_id, plate_map, echem_tech, scan_type)
sample_loc_dict,sample_comp_dict = plate_map_dict(plate_map)

I = {} # I = {sample number : 1d_array(I(A))}
for sample_number, CV2_file_path in sample_techfile_dict.items():    
    #if CV2_quality_check(CV2_file_path): # check if sample scan passes cv2 quality check
    with open(CV2_file_path) as f:
        txt = f.readlines()    
        current = np.zeros(shape=(len(txt[15:])))  
        for index,line in enumerate(txt[15:]):
            current[index] = float(line.split()[-2])
    I[sample_number] = current 
    
I_smooth = {sample_number:savgol_filter(current,5,2) for sample_number, current in I.items()}
I_resid_rmse = {sample_number:np.sqrt(np.sum(np.power(I[sample_number]-I_smooth[sample_number],2))/len(I)) for sample_number in I.keys()}

X = [sample_loc_dict[sample_number][0] for sample_number in I_resid_rmse]
Y = [sample_loc_dict[sample_number][1] for sample_number in I_resid_rmse]

plt.figure(figsize=(16,8))
plt.title('plate{}_{}PETS: I_resid_rmse(A)'.format(plate_id, scan_type))
sc = plt.scatter(X, Y, c=I_resid_rmse.values(), s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='I_resid_rmse(A)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    
plt.show()

#==============================================================================
# os.chdir(r"C:\Users\eche\Desktop\IPYNB\one-time analysis\190605_plate5052_analysis")
# with open('plate5052_postPETS_noise.csv', 'w') as f:
#     f.write('Sample_number,RMSE\n')
#     for key,value in I_resid_rmse.items():
#         f.write('{},{}\n'.format(key,value))
#==============================================================================
