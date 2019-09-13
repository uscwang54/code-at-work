# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:41:39 2019

@author: Yu Wang
"""

from glob import glob
import os
import re

# .done whose rcp needs to be fixed
done_folder_path = r"C:\INST\RUNS\20190131_MgCaFeYInLa_51466\20190201.165051.done" 

time_stamp = done_folder_path.split('\\')[-1].rstrip('.done')
rcp_file_path = glob(os.path.join(done_folder_path, '*.rcp'))[0] # rcp file that needs to be fixed

with open(rcp_file_path) as f:
    text = f.read()
    new_text = re.sub(r'.txt: t\(s\)', '.txt: eche_gamry_txt_file;t(s)', text)    
    
os.chdir(done_folder_path)

with open(time_stamp+'.rcp.fixed', 'w') as newfile:
    newfile.write(new_text)