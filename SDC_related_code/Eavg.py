# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:02:49 2019

@author: Yu
"""

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from Plate_Map import plate_map
from Plate_Sample_File import plate_sample_techfile

sample_loc_dict = plate_map(93) # needs to be updated  {sample_number:(x,y)}
sample_techfile_dict = plate_sample_techfile(5208, 93, 'CP4') # needs to be updated 
avg_time = 2 # needs to be updated (seconds from the end)
dt = 0.1 # time interval between two voltages

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
Eavg = {sample_number:np.mean(E_list[-int(avg_time/dt):]) for sample_number, E_list in E.items()} # Eavg = {sample number: Eavg(V)}

X,Y,Ea = [],[],[]
for sample_number in Eavg:
    X.append(sample_loc_dict[sample_number][0])
    Y.append(sample_loc_dict[sample_number][1])
    Ea.append(Eavg[sample_number])

sc = plt.scatter(X, Y, c=Ea, s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='E_avg (V)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    
