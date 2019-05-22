# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:58:09 2019

@author: eche
"""

from Plate_Sample_File import plate_sample_techfile
import numpy as np
import matplotlib.pyplot as plt

sample_techfile_dict = plate_sample_techfile(5210, 93, 'CV3') # needs to be updated 
techfile = sample_techfile_dict[10] # needs to be updated 

with open(techfile) as f:
    data = []
    for line in f:
        try:
            if type(eval(line.split('\t')[0]))==float:
                data.append(line)
        except SyntaxError:
            continue
    mydata = np.zeros((len(data),3))
    for index, line in enumerate(data):
        mydata[index,0] = float(line.split('\t')[0]) 
        mydata[index,1] = float(line.split('\t')[1]) 
        mydata[index,2] = float(line.split('\t')[-2]) 
      
t = mydata[:,0] # time in sec
V = mydata[:,1] # voltage in V
I = mydata[:,2] # current in A

fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(16,4))
for i,(x,y) in enumerate([(t,V),(t,I),(V,I)]):
    ax[i].plot(x,y)
    plt.tight_layout()
    
