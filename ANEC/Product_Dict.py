# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 09:06:55 2019

@author: anec
"""

import re

def product_dict(GC_liquid_result_file_path,GC_gas_result_file_path,HPLC_liquid_result_file_path):
    '''
    input: GC_liquid_result_file_path, GC_gas_result_file_path, HPLC_liquid_result_file_path
    output: entire product distribution for each fill
    '''

    GC_liquid_product_dict = {}
    with open(GC_liquid_result_file_path) as f:
        data = f.readlines()
        for index,line in enumerate(data):
            if re.search('^TOTAL', line.strip('\t')):
                break_line_index = index    
        mydata = data[10:break_line_index]
        for line in mydata:
            product_name = line.split('\t')[2]
            product_conc = line.split('\t')[-1].rstrip() #mM
            GC_liquid_product_dict[product_name] = product_conc
            
    GC_gas_product_dict = {}
    with open(GC_gas_result_file_path) as f:
        data = f.readlines()
        for index,line in enumerate(data):
            if re.search('^TOTAL', line.strip('\t')):
                break_line_index = index
        mydata = data[10:break_line_index]
        for line in mydata:
            FID_product_name = line.split("\t")[4]
            FID_product_conc = line.split("\t")[-2] #ppm
            GC_gas_product_dict[FID_product_name] = FID_product_conc
            TCD_product_name = line.split("\t")[5]
            TCD_product_conc = line.split("\t")[-1].rstrip() #ppm
            GC_gas_product_dict[TCD_product_name] = TCD_product_conc
            
    HPLC_liquid_product_dict = {}
    with open(HPLC_liquid_result_file_path) as f:
        data = f.readlines()
        for index,line in enumerate(data):
            if re.search('^TOTAL', line.strip('\t')):
                break_line_index = index    
        mydata = data[10:break_line_index]
        for line in mydata:
            product_name = line.split('\t')[2]
            product_conc = line.split('\t')[-1].rstrip() #mM
            HPLC_liquid_product_dict[product_name] = product_conc
            
    entire_product_dict = {}
    entire_product_dict.update(GC_liquid_product_dict)
    entire_product_dict.update(GC_gas_product_dict)
    entire_product_dict.update(HPLC_liquid_product_dict)
    
    return entire_product_dict
