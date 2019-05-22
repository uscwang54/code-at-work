# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:50:18 2018

@author: anec
"""

import os
from glob import glob

def gamry_files(expt_date):
    '''
    input: expt_date e.g., "181002"
    output: a list of gamry file paths conducted on the expt_date
    ''' 
    root_path = r"C:\Users\Public\Documents\My Gamry Data"  
    gamry_file_path = glob(os.path.join(root_path, expt_date+'*'))
    
    # some conditional selection if needed
    gamry_file_path = [file for file in gamry_file_path if 'Cu electro-polishing' not in file]
    
    return gamry_file_path
