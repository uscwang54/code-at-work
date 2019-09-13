# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 12:41:36 2019

@author: Yu Wang
"""

from __future__ import division
import sys
sys.path.append(r"C:\Users\eche\Desktop\IPYNB\Utility") #append the utility folder path
import matplotlib.pyplot as plt
import os
from Plate_Sample_File import plate_sample_techfile
from Quality_Check import CV2_quality_check
from Plate_Map import plate_map_dict

# plot the plate map with green dots representing good sample scans (judging from CV2)
# red dots representing bad sample scans (judging from CV2 quality)
# note: only run the script when SDC is not running

###################################################################################
parent_folder_path = r"C:\INST\RUNS\20190826_MnNiMgCaFeIn-postPETS_51624" #needs to be updated
###################################################################################

plate_id = int(os.path.basename(parent_folder_path).split("_")[-1][:-1])
plate_map = 69 #needs to be updated if necessary
echem_tech = 'CV2' #needs to be updated if necessary
scan_type = 'post' if 'post' in parent_folder_path else 'pre'

sample_techfile_dict = plate_sample_techfile(plate_id, plate_map, echem_tech, scan_type)
CV2_files = sample_techfile_dict.values() #list of all most recent cv2 files
total_sample_num = len(CV2_files)

sample_loc_dict, sample_comp_dict = plate_map_dict(plate_map)

X, Y, colors = [], [], [] # green for good sample; red for bad sample
counter = 0 # number of good samples
for CV2_file in CV2_files:
    sample_number = int(os.path.basename(CV2_file).split('_')[0].strip('Sample'))
    x,y = sample_loc_dict[sample_number]
    X.append(x)
    Y.append(y)
    if CV2_quality_check(CV2_file): #if cv2 file passes quality check
        colors.append('green')
        counter += 1
    else: #if cv2 file fails to pass quality check                    
        colors.append('red')
good_rate = counter/total_sample_num
bad_rate = 1-good_rate

plt.figure(figsize=(12,8))
plt.scatter(X,Y,color=colors)
plt.title('plate{}_{}PETS: {} good samples({:.2f}%) {} bad samples({:.2f}%)'.format(plate_id, scan_type, counter, 100*good_rate, total_sample_num-counter, 100*bad_rate))
plt.show()
