"""
Analysis of data from the DSLD noise study.
Use for plots in DSLD_plots.py

Am I doing the mean of the logs or the log of the means?
https://stats.stackexchange.com/questions/250209/log-mean-vs-mean-log-in-statistics

Ask Steve whether this is valid:
https://help.eagle.io/hc/en-au/articles/4770947081231-Calculating-a-logarithmic-mean-for-noise-data
i.e. take antilog of each value, average the anti-logs, then do the log of anti-log average

Via wikipedia (https://en.wikipedia.org/wiki/Decibel)
Acoustic decibles are:
decibles = 20*log10(p_meas,p_ref)

So I should be taking my decible measurements, dividing by 20, 10^that, then I'm at p_meas/p_ref... is p_ref 1?

Putting this in load_calc_data

Mike: what do the instrument's docs say?
Steve: is all that crap I found on the internet correct?

"""
import pandas as pd

def collection_high_stat(df,column_name):
	"""
	Extract the highest average noise recorded at the site, each day (each "collection")
	In practice you're iterating through the full code and getting the max of the means associated with each
	"""
	full_code_groups = df.groupby(['Full Code'])
	full_code_list = sorted(set(df['Full Code']))
	
	reduced_code_list = []
	for c in full_code_list:
		reduced_code_list.append(c[0:8]+c[-1])
	
	site_code_only_list = []
	for c in full_code_list:
		site_code_only_list.append(c[0:8])
	
	max_list = []
	time_code_list = [] # take this out to help with key group-bys later
	for code in full_code_list:
		max_list.append(max(full_code_groups.get_group(code)[column_name]))
		time_code_list.append(code[-1])
	# According to notes: use the highest average noise
	# At each location
	# At each day
	results = pd.DataFrame({
		"Full Code": full_code_list,
		"Time Code": time_code_list,
		"Reduced Code": reduced_code_list,
		"Site Code": site_code_only_list,
		"Max "+ column_name: max_list
		})
	return results

def take_larger_location_meas(df,column_name):
	df_list = []
	series_list = [] # I hate pandas. It doesn't correctly concat a list of series and DataFrames. Must be my fault.
	for thing in set(df['Reduced Code']):
		code_df = df.loc[(df['Reduced Code'] == thing)]

		if len(code_df) > 1:
			# oo.reset_index(drop=True)? The following feels dirty without this.
			i_max = code_df[column_name].idxmax()
			series_list.append(code_df.loc[i_max]) # HEY! Use iloc if you reset the index.
		
		else:
			df_list.append(code_df)
	#print('pd.concat(data_list)')
	#print(pd.concat(df_list))
	#print('pd.concat(series_list)')
	#print(pd.concat(series_list,axis=1).transpose())
	series_df = pd.concat(series_list,axis=1).transpose() # this is how you concat a list of series into a df non-stupidly.
	df_df = pd.concat(df_list)
	
	return pd.concat([series_df,df_df])

if __name__=='__main__':
	# Test the calculation functions above

	df = pd.read_csv('merged3.csv')
	results1 = collection_high_stat(df,'Log Mean (dB)')
	results1.to_csv('log_max_mean.csv')
	results2 = collection_high_stat(df,'Mean (dB)')
	results2.to_csv('max_mean.csv')
	results3 = take_larger_location_meas(results2,'Max Mean (dB)')
	results3 = results3.reset_index(drop=True)
	results3.to_csv('one_per_site.csv')
	
