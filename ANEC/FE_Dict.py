# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 09:31:16 2018

@author: anec
"""

def FE_dict(Q,product_dict,electrolyte):
    '''
    input: Q=coulomb of charge; product_dict=product distribution per fill; electrolyte='bicarbonate' or 'methanol'
    HS volume and liquid volume vary for two electrolyte systems
    output: FE distribution for each fill
    '''
    
    # Product of CO2RR along with the number of electrons needed to produce each one
    liquid_product_dict = {'Formate': 2,
     'Formic Acid': 2,
     'Methanol': 6,
     'Glyoxal': 6,
     'Acetate': 8,
     'Acetic Acid': 8,
     'Glycolaldehyde': 8,
     'Ethylene Glycol': 10,
     'Acetaldehyde': 10,
     'Ethanol': 12,
     'Hydroxyacetone': 14,
     'Acetone': 16,
     'Allyl Alcohol': 16,
     'Ally Alcohol' : 16,
     'Propionaldehyde': 16,
     '1-Propanol': 18,
     'Oxalic Acid': 2}
    
    gas_product_dict = {'H2': 2, 
     'Hydrogen': 2,
     'CO': 2, 
     'CH4': 8,
     'Methane': 8,
     'Ethylene': 12,
     'Ethane': 14}
    
    # Parameters and Constants for the calculations

    P = 1.0 # Pressure with unit: atm
    T = 298.15 # Temperature with unit: K
    R = 82.057338 # Gas constant with unit: cm3 atm K−1 mol−1
    FC = 96485.3329 # Faraday constant with unit: C/mole e-    
    if electrolyte=='methanol':
        V_HS = 2.940 # Cell headspace with unit: cm3
        V_liquid = 0.693 # Cell liquid with unit: cm3        
    elif electrolyte=='bicarbonate additive':
        V_HS = 2.675
        V_liquid = 1.200 
    elif electrolyte=='bicarbonate clean':
        V_HS =  3.210
        V_liquid = 0.790
        
                
    FE_dict = {}    
    for key in product_dict.keys():  
        
        if key.title() in gas_product_dict.keys():
            n = P*V_HS/(R*T) # Number of mole of gas(es) in the headspace with unit: mole
            FE_dict['FE_{}'.format(key.title())] = round(100*gas_product_dict[key.title()]*(product_dict[key]/1000000*n)/(Q/FC),2)
            
        elif key in ['H2','CO','CH4']:
            n = P*V_HS/(R*T) # Number of mole of gas(es) in the headspace with unit: mole
            FE_dict['FE_{}'.format(key)] = round(100*gas_product_dict[key]*(product_dict[key]/1000000*n)/(Q/FC),2)
            
        elif key.title() in liquid_product_dict.keys():
            FE_dict['FE_{}'.format(key.title())] = round(100*liquid_product_dict[key.title()]*(product_dict[key]/1000)*(V_liquid/1000)/(Q/FC),2)   
                           
       #else:
           #print("{} not found".format(key))    
            
   #FE_dict['FE_total']=round(sum(FE_dict.values()),2)
    
    return FE_dict
