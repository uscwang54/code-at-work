# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 10:56:40 2019

@author: eche
"""

import os
from glob import glob
import numpy as np
import re
import time
import smtplib
from smtpvars import mailuser,mailpass

parent_folder_path = r"C:\INST\RUNS\20190123_MgCaFeYInLa-postPETS_51477" # need to be changed for every new plate
run_folder_paths = glob(parent_folder_path + "\*.run") # all .run folders
ctimes = [os.path.getctime(run) for run in run_folder_paths] # list of all creation times of .run folders
ctimes = np.array(ctimes)
max_ind = ctimes.argmax() # the index of the max ctime among ctimes
run_folder_path = run_folder_paths[max_ind] # most recent .run folder under parent folder path

def return_cv2():
    '''
    check if there is new CV2.txt file added
    return the latest cv2 file path if it pops up
    otherwise, return None if keep checking for 600s
    '''   
    timer = 0
    while timer<600:
        cv2_files = glob(run_folder_path+'\*CV2*.txt')
        cv2_count = len(cv2_files)
        time.sleep(10)
        timer+=10
        new_cv2_files = glob(run_folder_path+'\*CV2*.txt')
        new_cv2_count = len(new_cv2_files)
        if cv2_count<new_cv2_count:
            return set(new_cv2_files).difference(set(cv2_files)).pop()
        else:
            time.sleep(10)
            timer+=10
            continue
    return None

            
def check_run():
    '''
    check if the most recent .run sub-folder still in the parent folder
    '''
    global run_folder_path
    sub_folders = [os.path.join(parent_folder_path, sub_folder) for sub_folder in os.listdir(parent_folder_path)]
    result = run_folder_path in sub_folders
    return result

            
def sendemail(subject):
    '''
    send message from a dummy gmail to designated email
    '''
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(mailuser,mailpass)
    from_addr = mailuser
    to_addrs = 'uscwang54@gmail.com'  
    msg = "Subject: " + subject
    smtp.sendmail(from_addr, to_addrs, msg)
    smtp.quit()

# complete rcp file only exists in .done or .copied folder
# need to manually generate one before runing the script, i.e. start/stop at the beginning of the experiment
done_folder_path = glob(parent_folder_path + "\*.done*")
copied_folder_path = glob(parent_folder_path + "\*.copied*")
# extend done_folder_path with copied_folder_path
done_folder_path.extend(copied_folder_path) 
# just grab .rcp file in the first .done or .copied folder if there is any
rcp_file_path = glob(done_folder_path[0] + "\*.rcp")[0] 
with open(rcp_file_path) as f:
    rcp_text = f.readlines()
    num_cycles_lines = []
    for line in rcp_text:
        if re.search(r'init_potential_vref', line):
            init_V = float(line.split()[-1])
        if re.search(r'first_potential_vref', line):
            final_V = float(line.split()[-1])
        if re.search(r'num_potential_cycles', line):
            num_cycles_lines.append(line)
            num_cycle = int(num_cycles_lines[0].split()[-1]) # 8 for pre-PETS; 3 for post-PETS
        
# machine generated Voltage vs time 
# potential sweep rate: 250 mV/s
# time data interval: 0.004 s, i.e. 250 data points/sec, every data piont covers 1 mV
sweep_rate = 0.250 # V/s
step_size = 0.001 # V
time_interval = 0.004 # sec
tot_time = 2*num_cycle*(init_V-final_V)/sweep_rate # every cycle contains downswing and upswing parts
t = np.arange(0, tot_time, time_interval) # time series/array
down_swing = np.arange(init_V, final_V, -step_size)
up_swing = np.arange(final_V, init_V, step_size)
cycle = np.concatenate((down_swing, up_swing))
voltage = np.tile(cycle, num_cycle) # voltage series/array

# take one point from every 100 points; reduce the array size
index = np.arange(0, len(t), 100)
t = np.array([t[i] for i in index])
t = np.append(t, tot_time) # refined time array
voltage = np.array([voltage[i] for i in index])
voltage = np.append(voltage, init_V) # refined voltage array

# Main loop to check folder increment/cv2 quality; send email if anything goes bad
while True:    
    cv2 = return_cv2()
    if cv2: # return the lastest cv2 file path if there is any
        with open(cv2) as f:
            txt = f.readlines()    
            data = np.zeros(shape=(len(txt[15:]), 2))  
            for index,line in enumerate(txt[15:]):
                data[index,0] = float(line.split()[0])
                data[index,1] = float(line.split()[1])

        t = data[:,0] # experimental t series
        v = data[:,1] # experimental v series
        index = np.arange(0, len(t), 100) # take one point from every 100 points
        t = np.array([t[i] for i in index]) # refined experimental t series
        v = np.array([v[i] for i in index]) # refined experimental v series

        difference = voltage - v # difference between the machine generated voltage series and exprimental results

        total = 0
        for diff in difference:
            total += np.power(diff, 2)
        div = np.sqrt(total)

        if div>0.1:
            print '{} went wrong!'.format(cv2.split('\\')[-1].split('_')[0]) 
            sendemail('The droplet goes bad on {}'.format(cv2.split('\\')[-1].split('_')[0]))
            continue
        else:
            print '{} success'.format(cv2.split('\\')[-1].split('_')[0])
            continue
            
    else: # if there is no new cv2 added 
        if check_run(): # .run folder still exits
            print 'SDC run has crashed or stalled'
            sendemail(subject='SDC run has crashed or stalled')
            break
        else: # .run folder no longer exits
            print 'SDC run has finished'
            sendemail(subject='SDC run has finished')
            break        