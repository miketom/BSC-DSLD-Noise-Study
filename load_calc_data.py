# Functions to load data and calculate statistics from the DSLD study data
# By Michael C. Thomas, 2024-01-29

# Time X: Bike the Drive
# Time A: Morning (8am-10am) during normal conditions 9-14 and 9-16
# Time B: Afternoon (3pm-5pm)
# Time C: Evening (8pm-5pm)

import pandas as pd
import numpy as np


def load_file_list(data_path,file_list):
	df_list = []
	for a_file in file_list:
		file_name = data_path + a_file
		df_list.append(pd.read_csv(file_name, keep_default_na=False))
		#print(len(df_list[-1]))
	df = pd.concat(df_list)
	return df


def dsld_data_config_dict():
	# Are you sure the config_dict gets used?
	config_dict = {}
	metadata_columns = ['7001',	'Site Code',	'Subsite Code',	'Date Code',	'Time Code',	'Full Code',	'Latitude',	'Longitude',	'Distance (ft)',	'Zip Code',	'Date (DD/MM/YYYY)',	'Start Time', 	'End Time',	'Temp. (F)',	'Humidity (%)',	'Wind Speed (mph)',	'Wind Direction',	'Barometer (in)',	'Dewpoint (F)',	'Visbility (mi)',	'Percipitation',	'Weather Time',	'Northbound Traffic',	'Southbound Traffic',	'Record Number']
	data_columns = ['Time - 0:10',	'Time - 0:20',	'Time - 0:30',	'Time - 0:40',	'Time - 0:50',	'Time - 1:00',	'Time - 1:10',	'Time - 1:20',	'Time -1:30']
	series_timestamps = [10,20,30,40,50,60,70,80,90]
	config_dict['metadata_columns'] = metadata_columns
	config_dict['data_columns'] = data_columns
	config_dict['series_timestamps'] = series_timestamps
	return config_dict

def delete_map_code_to_name(code):
	"""
	Delete: the subsites have names - I might not use this in the plot
	Map a site code like N-01-101 to the site name (Cricket Hill here)
	"""
	# Hard coded dict :P
	code_to_name_dict = {
	'N-01': 'Cricket Hill',
	'N-02': 'Belmont Rocks',
	'N-03': 'Oak Street Beach',
	'S-01': 'Oakwood Beach',
	'S-02': 'Promontory Point',
	'S-03': '63rd Street Beach',
	'Z-01': 'LFT Flyover',
	'Z-02': 'Buckingham Fountain'
	}
	return code_to_name_dict[code]

def calculate_run_statistics(data_df):	
	# Calculate the record statistics
	# TODO: use the outlier dict to gen the stats? No: these are all run characteristics
	# Outliers get used for later analysis to filter things out.
	median_list = []
	mean_list = []
	log_mean_list = []
	min_list = []
	max_list = []
	range_list = []
	std_list = []
	
	for i in range(len(data_df)):
		run_record = data_df.iloc[i]
		run_median = np.median(run_record)
		run_mean = np.mean(run_record) # "arithmatic" mean
		run_log_mean = acoustic_log_mean(run_record)
		run_min = np.min(run_record)
		run_max = np.max(run_record)
		run_range = run_max - run_min
		run_std = np.std(run_record)
		
		median_list.append(run_median)
		mean_list.append(run_mean)
		log_mean_list.append(run_log_mean)
		min_list.append(run_min)
		max_list.append(run_max)
		range_list.append(run_range)
		std_list.append(run_std)
		
	"""
	print(f'len(mean_list)={len(mean_list)}')
	print(f'len(median_list)={len(median_list)}')
	print(f'len(min_list)={len(min_list)}')
	print(f'len(max_list)={len(max_list)}')
	print(f'len(mean_list)={len(mean_list)}')
	"""
	stat_df = pd.DataFrame({
			"Mean (dB)": mean_list,
			"Log Mean (dB)": log_mean_list,
			"Median (dB)": median_list,
			"Minimum (dB)": min_list,
			"Maximum (dB)": max_list,
			"Range (dB)": range_list,
			"St. Deviation (dB)": std_list
			})
	return stat_df

def acoustic_log_mean(run_data):
	# decibles = 20*log10(p_meas,p_ref)
	anti_log_list = []
	for noise_db in run_data:
		anti_log_list.append(10**(noise_db/20)) # Confirmed correct, email with Steve 2/1/2024, he had 10's instead of 20's though	
	anti_log_mean = np.mean(anti_log_list)
	log_mean = 20*np.log10(anti_log_mean)
	return log_mean

def load_calc_data(data_path,file_list):
	# Bring all these functions together and output the data
	df = load_file_list(data_path,file_list)
	df = df.reset_index()
	config_dict = dsld_data_config_dict() # mainly IDs the columns with the noise data
	data_df = df[config_dict['data_columns']] # This just has the decible data
	stat_df = calculate_run_statistics(data_df)
	df = df.merge(stat_df,how='left', left_index=True, right_index=True) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
	return df

def filter_sites_by_distance(df):
	distance_limit = 500 # ft # source: noise assessment manual pdf pg 23/3-5 section 3.4
	filtered_df = df.loc[(df['Distance (ft)'] <= distance_limit)]
	return filtered_df

if __name__=='__main__':
	import matplotlib.pyplot as plt # Probably set a bunch of these off to the side
	#data_path = '../Data/N01 (Cricket Hill).csv'
	#data_path = '../Data/N02 (Belmont Rocks).csv'
	#df = pd.read_csv(data_path, keep_default_na=False)
	"""
	data_path = '../Data/'
	file_list = ['N01 (Cricket Hill).csv', 'N02 (Belmont Rocks).csv',\
				'N03 (Oak Street Beach).csv', 'Z01 (LFT Flyover).csv',\
				'Z02 (Buckingham Fountain).csv', 'S01 (Oakwood Beach).csv',\
				'S02 (Promontory Point).csv', 'S03 (63rd Street Beach).csv'\
				]
	"""
	data_path = '../Data/Decibel Records/'
	file_list = [ \
	'N01 (Cricket Hill) DLSD Noise Pollution Study Decible Readings.csv',\
	'N02 (Belmont Rocks) DLSD Noise Pollution Study Decible Readings.csv',\
	'N03 (Oak Street Beach) DLSD Noise Pollution Study Decible Readings.csv',\
	'S01 (Oakwood Beach) DLSD Noise Pollution Study Decible Readings.csv',\
	'S02 (Promontory Point) DLSD Noise Pollution Study Decible Readings.csv',\
	'S03 (63rd Street Beach) DLSD Noise Pollution Study Decible Readings.csv',\
	'Z01 (LFT Flyover) DLSD Noise Pollution Study Decible Readings.csv',\
	'Z02 (Buckingham Fountain) DLSD Noise Pollution Study Decible Readings.csv'\
	]

	#file_list = ['S02 (Promontory Point).csv', 'S03 (63rd Street Beach).csv']
	#file_list = ['S02 (Promontory Point).csv']
	df = load_file_list(data_path,file_list)
	#df.to_csv('df.csv') # Looks good here
	df = filter_sites_by_distance(df)
	df.to_csv('filtered.csv')

	df = df.reset_index(drop=True)
	# df.to_csv('reset.csv') # Looks good here
	
	config_dict = dsld_data_config_dict()
	data_df = df[config_dict['data_columns']] # This just has the decible data
	stat_df = calculate_run_statistics(data_df)
	#print(stat_df)
	#stat_df.to_csv('stat_df.csv') # This looked good.

	df = df.merge(stat_df,how='left', left_index=True, right_index=True) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
	df.to_csv('merged3.csv') # Looks good now
	
	fig, ax = plt.subplots(figsize=(8, 8))
	ax.scatter(df['Mean (dB)'],df['Log Mean (dB)'], marker='^', c='b', label='BTD')
	print(df['St. Deviation (dB)'])
	#ax.errorbar(df['Mean (dB)'],df['Log Mean (dB)'],yerr=df['St. Deviation (dB)'],uplims=True, lolims=True, linestyle='None') # Takeaway: Stdev isn't significant
	ax.set_title('Log Mean vs Mean')
	ax.set_xlabel('Mean (dB)')
	ax.set_ylabel('Log Mean (dB)')
	plt.show()
	########################################################################
	### Deal with outliers somewhere else?
	# Deal with data outliers
	i_bad_outliers = list(range(108,116+1)) + list(range(279,281+1)) # Expect these to be BAD bad
	i_commented = list(range(216,224+1))+list(range(228,230+1))+list(range(246,248+1))+list(range(255,257+1))+list(range(264,266+1))+list(range(271,272+1)) # not representative conditions
	# Add to the i_commented case - EVERYTHING with a comment should be in that list.

	outlier_dict = {'Bad':i_bad_outliers, 'Comment':i_commented}
	# Outlier analysis - mark, maybe throw away
	# Reason to throw away: plot with X or something
	# Keep anyway: plot with a star
	# Only throw away the beach volleyball I think
	# Beach volleyball - index 108 to 116 - throw away
	# Buckingham fountain - 216-224 also 228-230, 246-248, 255-257, 264-266, 
	# traffic event - 271-272 (was LSD closed for a bit?)
	# sea wall - 276-278, choppy water - 285-287, 294-296, 303-305, 312-314, 348-350
	# Trains passing? - 279-281
	# Beach water feature - 384-386
	########################################################################
	
