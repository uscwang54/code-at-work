# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 09:51:55 2018

@author: anec
"""

import os
from glob import glob

def chromeleon_files(expt_date):
    '''
    input: expt_date, e.g., "181002" 
    output: list of tuples, each tuple contains GC_liquid, GC_gas, HPLC_liquid result file paths for each fill
    '''
    root_path = glob(os.path.join(r"C:\Users\anec\Desktop\ECDataRepository", expt_date+"*"))[0]
    
    
    GC_liquid_result_file_path = glob(os.path.join(root_path, '*GC_Liquid_Results', '*.txt'))
    
    reordered_GC_liquid_result_file_path = []
    
    for index in range(len(GC_liquid_result_file_path)):
    
        for path in GC_liquid_result_file_path:
        
            if index+1==int(os.path.basename(path).split('.')[0]):
            
                reordered_GC_liquid_result_file_path.append(path)
                
    
    GC_gas_result_file_path = glob(os.path.join(root_path, '*GC_MultiHeadspace_Results', '*.txt'))
    
    reordered_GC_gas_result_file_path = []
    
    for index in range(len(GC_gas_result_file_path)):
        
        for path in GC_gas_result_file_path:
            
            if index+1==int(os.path.basename(path).split('.')[0]):
                
                reordered_GC_gas_result_file_path.append(path)
    
       
    HPLC_liquid_result_file_path = glob(os.path.join(root_path, '*HPLC_Results', '*.txt'))
    
    reordered_HPLC_liquid_result_file_path = []
    
    for index in range(len(HPLC_liquid_result_file_path)):
        
        for path in HPLC_liquid_result_file_path:
            
            if index+1==int(os.path.basename(path).split('.')[0]):
                
                reordered_HPLC_liquid_result_file_path.append(path)
                
    
    if len(GC_liquid_result_file_path)==len(GC_gas_result_file_path)==len(HPLC_liquid_result_file_path):
        
        return list(zip(reordered_GC_liquid_result_file_path,
                        reordered_GC_gas_result_file_path,
                        reordered_HPLC_liquid_result_file_path))
        
    else:
        
        return 'The number of GC_liquid, GC_gas, HPLC_liquid result files are not equal.'
