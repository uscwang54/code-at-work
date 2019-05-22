# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 11:15:30 2018

@author: anec
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Gamry_Files import gamry_files

def figure_generator(expt_date, num_of_fills_per_sample):
    '''
    generate I vs t and V vs t, per each eletrolysis data recorded in Gamry .DTA based on expt. date
    '''
    
    gamry_file_path = gamry_files(expt_date)
    
    dfs = []
    for file in gamry_file_path:
        with open(file) as f:
            data=f.readlines()
            mydata=data[68:] # read from line 69, will need to change this for different types of files  
            new_data = np.zeros((len(mydata),3))
            for i in range(len(mydata)):    
                new_data[i]=mydata[i].split("\t")[2:5]
       
            df = pd.DataFrame(new_data)
            df.columns=['Time(s)','V vs. Ref.(V)','I(A)']
            dfs.append(df)
            
        
    # dynamically plot m*n grid plot, N=number of fills per sample, M=number of samples

    N = num_of_fills_per_sample # need to adjust for individual experiment
    M = int(len(dfs)/N) # number of samples
    
    fig, ax = plt.subplots(nrows=M, ncols=N, figsize=(16,4*M))    
    if M == 1:
        for j in range(N):
            
            ax[j].plot(dfs[j]['Time(s)'][1:], 1000*dfs[j]["I(A)"][1:], 'b.')
            ax[j].set_xlabel('Time(s)')
            ax[j].set_ylabel('Current (mA)',color='b') 
            ax[j].set_ylim([-4,0])
            ax[j].tick_params(axis='y', labelcolor='b')
            ax[j].set_title("sample {}: fill {}".format(M, j+1))
            ax_twin = ax[j].twinx()
            ax_twin.plot(dfs[j]['Time(s)'][1:], dfs[j]["V vs. Ref.(V)"][1:], 'r.')
            ax_twin.set_ylabel('Voltage vs. Ref (V)',color='r')
            ax_twin.set_ylim([-3.0,0])
            ax_twin.set_yticks([-3.0,-2.5,-2,-1.5,-1,-0.5,0])
            ax_twin.tick_params(axis='y', labelcolor='r')
            fig.tight_layout()
            plt.savefig('Voltage_Current_Time.jpeg')

            
    elif M > 1:
        
        if N>1:
            for i in range(M):
                for j in range(N):
                    ax[i,j].plot(dfs[i*N+j]['Time(s)'][1:], 1000*dfs[i*N+j]["I(A)"][1:], 'b.')
                    ax[i,j].set_xlabel('Time(s)')
                    ax[i,j].set_ylabel('Current (mA)',color='b')
                    ax[i,j].set_ylim([-5,0])
                    ax[i,j].tick_params(axis='y', labelcolor='b')
                    ax[i,j].set_title(f"sample {i+1}: fill {j+1}")
                    ax_twin = ax[i,j].twinx()
                    ax_twin.plot(dfs[i*N+j]['Time(s)'][1:], dfs[i*N+j]["V vs. Ref.(V)"][1:], 'r.')
                    ax_twin.set_ylabel('Voltage vs. Ref (V)',color='r')
                    ax_twin.set_ylim([-2.5,0])
                    ax_twin.set_yticks([-2.5,-2,-1.5,-1,-0.5,0])
                    ax_twin.tick_params(axis='y', labelcolor='r')
                    plt.tight_layout()
                    plt.savefig('Voltage_Current_Time.jpeg')
                    
        elif N==1:
            for i in range(M):
                ax[i].plot(dfs[i]['Time(s)'][1:], 1000*dfs[i]["I(A)"][1:], 'b.')
                ax[i].set_xlabel('Time(s)')
                ax[i].set_ylabel('Current (mA)',color='b') 
                ax[i].set_ylim([-4,0])
                ax[i].tick_params(axis='y', labelcolor='b')
                ax[i].set_title("sample {}: fill {}".format(i+1, N))
                ax_twin = ax[i].twinx()
                ax_twin.plot(dfs[i]['Time(s)'][1:], dfs[i]["V vs. Ref.(V)"][1:], 'r.')
                ax_twin.set_ylabel('Voltage vs. Ref (V)',color='r')
                ax_twin.set_ylim([-3.0,0])
                ax_twin.set_yticks([-3.0,-2.5,-2,-1.5,-1,-0.5,0])
                ax_twin.tick_params(axis='y', labelcolor='r')
                fig.tight_layout()
                plt.savefig('Voltage_Current_Time.jpeg')
                
  