# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 20:45:40 2019

@author: anec
"""

from collections import defaultdict
from Chromeleon_Files import chromeleon_files
from Product_Dict import product_dict

def product_sum(expt_date,num_of_fills_per_sample):
    '''
    input: expt_date,num_of_fills_per_sample
    output: product distribution summary for each and every fill
    '''

    fills_analytical_results = chromeleon_files(expt_date) # list of tuples, each tuple contains GC_liquid, GC_gas, HPLC_liquid result file paths for each fill
    num_of_samples = int(len(fills_analytical_results)/num_of_fills_per_sample)
    
    product_summary = defaultdict(dict)
    
    sample_fill_name_list = []
    for i in range(num_of_samples):
        for j in range(num_of_fills_per_sample):
            sample_fill_name_list.append('Sample{}_fill{}'.format(i+1,j+1))
            
    for index, item in enumerate(sample_fill_name_list):
        product_summary[item] = product_dict(*fills_analytical_results[index])
        
    return product_summary