def chromeleon_files(expt_date) 
output a list of tuples, each tuple consists of all the chromeleon exported .txt file paths for each fill conducted on the expt_date


def product_dict(GC_liquid_result_file_path,GC_gas_result_file_path,HPLC_liquid_result_file_path)
output a dictionary of the entire product distribution for each fill


def product_sum(expt_date,num_of_fills_per_sample)
output a dictionary of product distribution summary for each and every fill

----------------------------------------------------------------------------------------------------

def gamry_files(expt_date)
output a list of gamry exported .DTA file paths for each fill conducted on the expt_date


def coulomb_sum(expt_date,num_of_fills_per_sample)
output a dictionary of coulomb calculation summary for each and every fill

----------------------------------------------------------------------------------------------------

def FE_dict(Q,product_dict,electrolyte)
input: Q=coulomb of charge per fill; product_dict=product distribution per fill; electrolyte='bicarbonate' or 'methanol'
(HS volume and liquid volume vary for two electrolyte systems)
output a dictionary of FE distribution for each fill

FE_summary_MainScript.py
output: a dataframe of summary of each and every fill's product distribution, write to excel under the associated ECDataRepository subfolder
	a dataframe of summary of each and every fill's FE distribution based on the following rules:
# 1. the product has to be in the product_priority list
# 2. the FE of the product itself has to be less than 120%
# 3. the total_FE of all the products has to be less than 150%
	write to excel under the associated ECDataRepository subfolder
	a .jpeg figure plotted Voltage, current vs. time

----------------------------------------------------------------------------------------------------

def figure_generator(expt_date, num_of_fills_per_sample)
output I vs t and V vs t, for each and every fill conducted on the expt_date
