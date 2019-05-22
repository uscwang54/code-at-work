# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 09:40:43 2018

@author: anec
"""

'''
input = expt_date
output = the averaged voltage of each gamry CPs performed on the expt_date
'''

import pandas as pd
import numpy as np
from Gamry_Files import gamry_files

def avg_volage_cal(expt_date):

    gamry_file_path = gamry_files(expt_date)
    
    dfs = []
    
    for file in gamry_file_path:
        
        with open(file) as f:
            
            data=f.readlines()
            
            data=data[68:] # read from line 69, i.e. first line of data in the DTA file
            
            new_data = np.zeros((len(data),3))
            
            for i in range(len(data)):
                
                new_data[i]=data[i].split("\t")[2:5]
                
            df = pd.DataFrame(new_data)
            
            df.columns=['Time(s)','V vs. Ref.(V)','I(A)']
            
            dfs.append(df)
            
    vol = []
    
    for df in dfs:   
        if df.shape[0] < 300:
            vol.append(np.mean(df['V vs. Ref.(V)'][150:]))
            
        elif df.shape[0] > 800:
            vol.append(np.mean(df['V vs. Ref.(V)'][500:]))
                     
    return vol
        


