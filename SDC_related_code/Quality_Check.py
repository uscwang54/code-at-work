# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:10:00 2019

@author: Yu Wang
"""

# voltage check of the CV2 files
import os
import re
import numpy as np
from glob import glob

def CV2_quality_check(CV2_file_path):
    '''
    check the quality of a given CV2 file
    
    input: CV2 file path
    output: True if CV2 passes quality check; False otherwise
    '''   
    folder_contain_CV2 = os.path.dirname(CV2_file_path)
    rcp = glob(os.path.join(folder_contain_CV2, "*.rcp"))[0]
    
    with open(rcp) as f:
        text = f.readlines()
        for i, line in enumerate(text):
            if re.search(r'^echem_params__CV2:',line):
                CV2_start_index = i+1
                break
            
    CV2_params = text[CV2_start_index:CV2_start_index+14] # there are 14 params for CV tech
    for line in CV2_params: 
        if re.search(r'init_potential_vref', line):
            init_V = float(line.split()[-1])
        if re.search(r'first_potential_vref', line):
            final_V = float(line.split()[-1])
        if re.search(r'num_potential_cycles', line):
            num_cycle = int(line.split()[-1])
        if re.search(r'potential_sweep_rate', line):
            sweep_rate = float(line.split()[-1])  
        if re.search(r'acquisition_vinterval', line):
            step_size = float(line.split()[-1])
                
    # machine generated Voltage vs time 
    # potential sweep rate: 250 mV/s
    # time data interval: 0.004 s, i.e. 250 data points/sec, every data piont covers 1 mV
    time_interval = step_size/sweep_rate # 0.004 sec time interval between data pionts
    tot_time = 2*num_cycle*(init_V-final_V)/sweep_rate # every cycle contains downswing and upswing parts
    t = np.arange(0, tot_time, time_interval) # time series/array
    down_swing = np.arange(init_V, final_V, -step_size)
    up_swing = np.arange(final_V, init_V, step_size)
    cycle = np.concatenate((down_swing, up_swing))
    voltage = np.tile(cycle, num_cycle) # voltage series/array
    
    # take one point from every 100 points; reduce the array size
    index = np.arange(0, len(t), 100)
    t = np.array([t[i] for i in index])
    t = np.append(t, tot_time) # refined time array
    voltage = np.array([voltage[i] for i in index])
    voltage = np.append(voltage, init_V) # refined voltage array
    
    # check if the experiment genrated voltage series matches with the machine generated voltage array
    with open(CV2_file_path) as f:
        txt = f.readlines()    
        data = np.zeros(shape=(len(txt[15:]), 3))  
        for index,line in enumerate(txt[15:]):
            data[index,0] = float(line.split()[0])
            data[index,1] = float(line.split()[1])
            data[index,2] = float(line.split()[-2])
    
    t = data[:,0] # experimental t series
    v = data[:,1] # experimental v series
    I = data[:,2] # experimental i series
    index = np.arange(0, len(t), 100) # take one point from every 100 points
    t = np.array([t[i] for i in index]) # refined experimental t series
    v = np.array([v[i] for i in index]) # refined experimental v series
    
    difference = voltage - v # difference between the machine generated voltage series and exprimental results
    
    total = 0
    for diff in difference:
        total += np.power(diff, 2)
    div = np.sqrt(total)
    
    if div>0.1 or np.max(I)<1.e-7: #either voltage profile or current went wrong
        return False
    else:
        return True
