# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:14:12 2019

@author: eche
"""

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from Plate_Map import plate_map
from Plate_Sample_File import plate_sample_techfile

sample_loc_dict = plate_map(84) # needs to be updated  {sample_number:(x,y)}
sample_techfile_dict = plate_sample_techfile(3282, 84, 'CA2') # needs to be updated 
avg_time = 2 # needs to be updated (seconds from the end)
dt = 0.1 # time interval between two voltages

I = defaultdict(list) # E = {sample number : [I(A)]}
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
        I[sample_number].append(float(line.split('\t')[-2])) 
Iavg = {sample_number:np.mean(I_list[-int(avg_time/dt):]) for sample_number, I_list in I.items()} # Iavg = {sample number: Iavg(A)}

X,Y,Ia = [],[],[]
for sample_number in Iavg:
    X.append(sample_loc_dict[sample_number][0])
    Y.append(sample_loc_dict[sample_number][1])
    Ia.append(Iavg[sample_number])

plt.figure(figsize=(10,6))
sc = plt.scatter(X, Y, s=35, c=Ia, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='I_avg (A)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    