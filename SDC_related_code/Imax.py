# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:31:46 2019

@author: eche
"""

from collections import defaultdict
import matplotlib.pyplot as plt
from Plate_Map import plate_map
from Plate_Sample_File import plate_sample_techfile

sample_loc_dict = plate_map(69) # needs to be updated  {sample_number:(x,y)}
sample_techfile_dict = plate_sample_techfile(5146, 69, 'CV2') # needs to be updated 

I = defaultdict(list) # I = {sample number : [I(A)]}
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
Imin = {sample_number:np.max(I_list) for sample_number, I_list in I.items()} # Imin = {sample number: Imin(A)}

X,Y,Im = [],[],[]
for sample_number in Imin:
    X.append(sample_loc_dict[sample_number][0])
    Y.append(sample_loc_dict[sample_number][1])
    Im.append(Imin[sample_number])

plt.figure(figsize=(16,10))
sc = plt.scatter(X, Y, c=Im, s=35, marker='s', cmap='RdYlBu')
plt.colorbar(sc, label='I_max (A)')
plt.tick_params(axis='both',          
    which='both',      
    bottom=False,     
    left=False,         
    labelbottom=False,
    labelleft=False)    