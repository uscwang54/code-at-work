# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 13:48:20 2018

@author: anec
"""

import numpy as np
import pandas as pd
from Gamry_Files import gamry_files

def coulomb_sum(expt_date,num_of_fills_per_sample):
    '''
    calculate total coulomb of charge passed per each electrolysis data recorded in Gamry .DTA 
    input: expt_date, num_of_fills_per_sample
    output: a dict of coulomb calculation summary for each and every fill
    '''
    
    gamry_file_path = gamry_files(expt_date)
    
    dfs = []
    for file in gamry_file_path:
        with open(file) as f:
            data=f.readlines()
            mydata=data[68:] # read from line 69, i.e. first line of data in the DTA file
            new_data = np.zeros((len(mydata),3))           
            for i in range(len(mydata)):              
                new_data[i]=mydata[i].split("\t")[2:5]   
            df = pd.DataFrame(new_data)           
            df.columns=['Time(s)','V vs. Ref.(V)','I(A)']           
            dfs.append(df)
                
    Q = []   
    for i, df in enumerate(dfs):       
        q = round(-1*df['I(A)'][1:].sum(), 4) # based on the fact that the time interval is 1 sec       
        Q.append(q)
    
    num_of_samples = int(len(Q)/num_of_fills_per_sample)    
    sample_fill_name_list = []
    for i in range(num_of_samples):
        for j in range(num_of_fills_per_sample):
            sample_fill_name_list.append('Sample{}_fill{}'.format(i+1,j+1))
    
    coulomb_summary = {}        
    for index, item in enumerate(sample_fill_name_list):
        coulomb_summary[item] = Q[index]     
        
    return coulomb_summary
    
    
        
