# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:28:25 2019

@author: eche
"""

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from Plate_Map import plate_map
from Plate_Sample_File import plate_sample_techfile

sample_loc_dict = plate_map(69) # needs to be updated  {sample_number:(x,y)}
sample_techfile_dict = plate_sample_techfile(5136, 69, 'CV2') # needs to be updated 

E = defaultdict(list) # E = {sample number : [E(V)]}
for sample_number, techfile in sample_techfile_dict.items():    
    with open(techfile) as f:
        data = []
        for line in f:
            try:
                if type(eval(line.split('\t')[0]))==float:
                    data.append(line)
            except SyntaxError:
                continue
    for line in data:
        E[sample_number].append(float(line.split('\t')[1])) 
Emin = {sample_number:np.max(E_list) for sample_number, E_list in E.items()} # Emin = {sample number: Emin(V)}

X,Y,Em = [],[],[]
for sample_number in Emin:
    X.append(sample_loc_dict[sample_number][0])
    Y.append(sample_loc_dict[sample_number][1])
    Em.append(Emin[sample_number])

plt.figure(figsize=(16,10))
sc = plt.scatter(X, Y, c=Em, s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='E_max (V)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    