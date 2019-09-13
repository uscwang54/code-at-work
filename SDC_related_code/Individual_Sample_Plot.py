# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:58:09 2019

@author: Yu Wang
"""

from Plate_Sample_File import plate_sample_techfile
import numpy as np
import matplotlib.pyplot as plt

def plot_sample(plate_id, plate_map, echem_tech, scan_type, sample_number):
    '''
    plot echem data (e.g. 'CA1','CV2') for the specified sample_number from a given plate
    
    input: plate_id (int: 4 digit), plate_map (int: 2 digit), echem_tech (string:, e.g. 'CV2'), 
           scan_type (string:'pre' or 'post'), sample_number(int)
    output: 3 figures of potential vs. time, current vs. time, potential vs. current
    '''
    sample_techfile_dict = plate_sample_techfile(plate_id, plate_map, echem_tech, scan_type) 
    techfile = sample_techfile_dict[sample_number]
    
    with open(techfile) as f:
        data = []
        for line in f:
            try:
                if type(eval(line.split('\t')[0]))==float:
                    data.append(line)
            except SyntaxError:
                continue
        mydata = np.zeros((len(data),3))
        for index, line in enumerate(data):
            mydata[index,0] = float(line.split('\t')[0]) 
            mydata[index,1] = float(line.split('\t')[1]) 
            mydata[index,2] = float(line.split('\t')[-2]) 
          
    t = mydata[:,0] # time in sec
    V = mydata[:,1] # voltage in V
    I = mydata[:,2] # current in A
    
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(16,4))
    ax[0].plot(t,V)
    ax[0].set_xlabel('time (s)')
    ax[0].set_ylabel('Potential vs. Reference (V)')
    
    ax[1].plot(t,I)
    ax[1].set_xlabel('time (s)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_title("Sample{0} from plate{1} {2}_{3}PETS".format(sample_number, plate_id, echem_tech, scan_type), fontsize=16)
    
    ax[2].plot(V,I)
    ax[2].set_xlabel('Potential vs. Reference (V)')
    ax[2].set_ylabel('Current (A)')
    plt.tight_layout()
    plt.show()
    

