# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 15:37:42 2018

@author: anec
"""

# main script to run to get the charge (coulomb passed), CO2RR product distribution, FE distribution for each fill
from collections import defaultdict
from glob import glob
import pandas as pd
import os
from Coulomb import coulomb_sum
from Product_Summary import product_sum
from FE_Dict import FE_dict
from Figure_Generator import figure_generator

expt_date = '190311' # need to be updated
num_of_fills_per_sample = 1 # need to be updated
product_summary = product_sum(expt_date, num_of_fills_per_sample) 
# dict of product distribution for each fill: 'Sample1_fill1': {'H2':10000,'CO':5000,...},...,'Sample1_fill3':{}...
coulomb_summary = coulomb_sum(expt_date, num_of_fills_per_sample)
# dict of coulombs for each fill: 'Sample1_fill1': 0.8,...,'Sample1_fill3':0.6...
electrolyte = 'bicarbonate' # need to be updated, 'bicarbonate' or 'methanol'

        
FE_summary = defaultdict(dict)
for key, value in coulomb_summary.items():
    Q = value
    product_dict = product_summary[key]
    product_dict = {k:float(v) for k,v in product_dict.items() if v!='n.a.'}
    FE_result = FE_dict(Q,product_dict,electrolyte)
    FE_summary[key] = FE_result
    
product_priority =['H2','Hydrogen','CO','Methanol','Acetaldehyde','Ethanol',
                   'CH4','Methane','Ethylene','Ethane','Formic Acid','Formate','Glyoxal','Oxalic Acid',
                   'Propionaldehyde','Allyl Alcohol'] # need to be updated if target products change

# refine FE_summary based on the following rules:
# 1. the product has to be in the product_priority list
# 2. the FE of the product itself has to be less than 120%
# 3. the total_FE of all the products has to be less than 150%
refined_FE_summary = defaultdict(dict)
for key, FE_dictionary in FE_summary.items():
    total_FE = 0
    for product, FE in FE_dictionary.items():
        if product.split('_')[1] in product_priority and FE<120 and total_FE<150:
            refined_FE_summary[key][product] = FE
            total_FE += FE
    refined_FE_summary[key]['FE_total'] = total_FE
    
refined_product_summary = defaultdict(dict)
for key, product_dict in product_summary.items():
    for product,conc in product_dict.items():
        if 'FE_'+product.title() in refined_FE_summary[key].keys() or 'FE_'+product in ['FE_H2','FE_CO','FE_CH4']:
            refined_product_summary[key][product] = conc

df_product_summary = pd.DataFrame(refined_product_summary).transpose()
df_FE_summary = pd.DataFrame(refined_FE_summary).transpose()

if __name__ == '__main__':
    destination_dir = glob(os.path.join(r"C:\Users\anec\Desktop\ECDataRepository", expt_date+"*"))[0]
    os.chdir(destination_dir)
    
    with pd.ExcelWriter('product_analyses.xlsx') as writer:
        df_product_summary.to_excel(writer, sheet_name='product_summary', na_rep='n.a.')
        df_FE_summary.to_excel(writer, sheet_name='FE_summary', na_rep='n.a.')
        
    figure_generator(expt_date, num_of_fills_per_sample)
    

            
    
                
        
        
    
        


