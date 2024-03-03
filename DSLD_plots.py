"""
Coding the plots for the DSLD Noise Study

Questions:
When should you wear ear protection?
ANOVA? PCA? What more advanced analysis should we perform?
Covariance matrix (nah)

Remove outliers based on video comments
Color by BTD vs normal traffic
SCatter of distance to LSD, humidity, wind, (we	ather effects)

Fish for:
Quantify the noise increase of Bike the Drive vs normal traffic
When is the noisiest traffic time

https://noiseawareness.org/


"""
import load_calc_data as loading
import analysis

import matplotlib.pyplot as plt # Probably set a bunch of these off to the side


def noise_vs_distance_plot(df):
	traffic_groups = df.groupby(['Northbound Traffic'])
	x_column = 'Distance (ft)'
	y_column = 'Mean (dB)'

	fig, ax = plt.subplots(figsize=(18, 6))
	ax.scatter(traffic_groups.get_group('BTD')[x_column], traffic_groups.get_group('BTD')[y_column], marker='^', c='b', label='BTD')
	ax.scatter(traffic_groups.get_group('GREEN')[x_column], traffic_groups.get_group('GREEN')[y_column], marker='o', c='g', label='GREEN')
	ax.scatter(traffic_groups.get_group('ORANGE')[x_column], traffic_groups.get_group('ORANGE')[y_column], marker='o', c='y', label='ORANGE')
	ax.scatter(traffic_groups.get_group('RED')[x_column], traffic_groups.get_group('RED')[y_column], marker='o', c='r', label='RED')
	ax.scatter(traffic_groups.get_group('DARK RED')[x_column], traffic_groups.get_group('DARK RED')[y_column], marker='o', c='k', label='DARK RED')
	ax.set_xlim([0,600]) # Just looks flat when you add this. 0 dB noise isn't realistic anyway.
	#ax.set_ylim([0,80])
	ax.set_xlabel(x_column)
	ax.set_ylabel(y_column)
	ax.legend()
	ax.set_title('Mean Noise vs Distance, by traffic')
	plt.show()

def noise_vs_distance_plot_with_redline(df):
	traffic_groups = df.groupby(['Northbound Traffic'])
	x_column = 'Distance (ft)'
	y_column = 'Mean (dB)'

	fig, ax = plt.subplots(figsize=(18, 6))
	ax.scatter(traffic_groups.get_group('BTD')[x_column], traffic_groups.get_group('BTD')[y_column], marker='^', c='b', label='BTD')
	ax.scatter(traffic_groups.get_group('GREEN')[x_column], traffic_groups.get_group('GREEN')[y_column], marker='o', c='g', label='GREEN')
	ax.scatter(traffic_groups.get_group('ORANGE')[x_column], traffic_groups.get_group('ORANGE')[y_column], marker='o', c='y', label='ORANGE')
	ax.scatter(traffic_groups.get_group('RED')[x_column], traffic_groups.get_group('RED')[y_column], marker='o', c='r', label='RED')
	ax.scatter(traffic_groups.get_group('DARK RED')[x_column], traffic_groups.get_group('DARK RED')[y_column], marker='o', c='k', label='DARK RED')
	
	ax.plot([0,600,1600],[66,66,66],'r-')
	ax.set_xlim([0,600]) # Just looks flat when you add this. 0 dB noise isn't realistic anyway.
	#ax.set_ylim([0,80])
	ax.set_xlabel(x_column)
	ax.set_ylabel(y_column)
	ax.legend()
	ax.set_title('Mean Noise vs Distance, by traffic')
	plt.show()

def lognoise_vs_distance_plot_with_redline(df):
	traffic_groups = df.groupby(['Northbound Traffic'])
	x_column = 'Distance (ft)'
	y_column = 'Log Mean (dB)'

	fig, ax = plt.subplots(figsize=(18, 6))
	ax.scatter(traffic_groups.get_group('BTD')[x_column], traffic_groups.get_group('BTD')[y_column], marker='^', c='b', label='BTD')
	ax.scatter(traffic_groups.get_group('GREEN')[x_column], traffic_groups.get_group('GREEN')[y_column], marker='o', c='g', label='GREEN')
	ax.scatter(traffic_groups.get_group('ORANGE')[x_column], traffic_groups.get_group('ORANGE')[y_column], marker='o', c='y', label='ORANGE')
	ax.scatter(traffic_groups.get_group('RED')[x_column], traffic_groups.get_group('RED')[y_column], marker='o', c='r', label='RED')
	ax.scatter(traffic_groups.get_group('DARK RED')[x_column], traffic_groups.get_group('DARK RED')[y_column], marker='o', c='k', label='DARK RED')
	
	ax.plot([0,600,1600],[66,66,66],'r-')
	ax.set_xlim([0,600]) # Just looks flat when you add this. 0 dB noise isn't realistic anyway.
	#ax.set_ylim([0,80])
	ax.set_xlabel(x_column)
	ax.set_ylabel(y_column)
	ax.legend()
	ax.set_title('Mean Noise vs Distance, by traffic')
	plt.show()

def bar_plot_by_time_code(max_log_means, plot_title):
	# this version plots two bars, one colored by SB traffic, the other by NB traffic 
	max_log_means = max_log_means.sort_values('Full Code')
	fig, ax = plt.subplots(figsize=(18, 6))
	width = 10
	multiplier = 1.1
	i_bar = 0
	label_pos = []
	bar_labels = []
	bar_color_reference = {'X':'tab:blue','A':'tab:red','B':'tab:orange','C':'tab:purple'}

	for i in range(0,len(max_log_means)):#attribute, measurement in penguin_means.items():
		#if max_log_means['Time Code'].iloc[i]=='X':
		#print(i)
		#print(i_bar)
		#print(max_log_means['Max Log Mean (dB)'].iloc[i])
		
		attribute = str(i) # make this the location name?
		i_bar = i_bar + 1
		offset = width * multiplier
		x = i_bar + offset
		
		measurement = max_log_means['Max Log Mean (dB)'].iloc[i]
		bar_label = max_log_means['Full Code'].iloc[i][0:8]
		#map_code_to_name(code) # might not use this
		bar_labels.append(bar_label)
		label_pos.append(x)
		
		the_bar = ax.bar(x, round(measurement), width, label=bar_label,color='tab:blue')
		ax.bar_label(the_bar, padding=3)
		
		multiplier += 1
	ax.set_xticks(label_pos, labels=bar_labels, rotation='vertical')
	plt.subplots_adjust(bottom=0.3)
	ax.set_xlabel('Site')
	ax.set_ylabel('Measured Noise (dB)')
	ax.set_title(plot_title)
	ax.set_ylim([30,90])

	# The IDOT abatement approach value
	IDOT_approach_db = 66
	ax.axhline(y=IDOT_approach_db, color="red")
	ax.text(-3,66, "{:.0f} db".format(IDOT_approach_db), color="red",ha="left", va="bottom")
	# From: https://stackoverflow.com/questions/42877747/add-a-label-to-y-axis-to-show-the-value-of-y-for-a-horizontal-line-in-matplotlib
	return 0

def time_code_traffic_bar(max_log_means, plot_title, traffic_lookup_dict):
	# Bar plot of the max log means of each site, bars split in two and colored
	# based on the Google Maps traffic.
	# Matplotlib bar plot demos: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
	max_log_means = max_log_means.sort_values('Full Code')
	fig, ax = plt.subplots(figsize=(18, 6))
	width = 10
	multiplier = 1.1
	i_bar = 0
	label_pos = []
	bar_labels = []
	traffic_color_lookup = {'BTD':'tab:blue', 'GREEN':'tab:green', 'ORANGE':'tab:orange', 'RED':'tab:red','DARK RED':'tab:brown'}
	
	for i in range(0,len(max_log_means)): # attribute, measurement in penguin_means.items():
		attribute = str(i) # make this the location name?
		i_bar = i_bar + 1
		offset = width * multiplier
		x = i_bar + offset
		
		measurement = max_log_means['Max Log Mean (dB)'].iloc[i]
		bar_label = max_log_means['Full Code'].iloc[i][0:8]
		bar_labels.append(bar_label)
		label_pos.append(x)
		
		if max_log_means['Full Code'].iloc[i][-1] == 'X':
			the_bar = ax.bar(x, round(measurement), width, label=bar_label,color='tab:blue')
			ax.bar_label(the_bar, padding=3)
		else:
			nobo_traffic = traffic_lookup_dict[max_log_means['Full Code'].iloc[i]]['Northbound Traffic']
			sobo_traffic = traffic_lookup_dict[max_log_means['Full Code'].iloc[i]]['Southbound Traffic']
			nobo_traffic_color = traffic_color_lookup[nobo_traffic]
			sobo_traffic_color = traffic_color_lookup[sobo_traffic]
			
			the_bar0 = ax.bar(x, 0, width, label=bar_label,color='tab:blue') # just for the label
			x1 = i_bar + offset - 0.25*width
			x2 = i_bar + offset + 0.25*width
			the_bar = ax.bar(x1, round(measurement), width/2, label=bar_label,color=sobo_traffic_color) # southbound on the left b/c 'MERICA!
			the_bar2 = ax.bar(x2, round(measurement), width/2, label=bar_label,color=nobo_traffic_color)
			ax.bar_label(the_bar0, padding=3)
		
		multiplier += 1
	ax.set_xticks(label_pos, labels=bar_labels, rotation='vertical')
	plt.subplots_adjust(bottom=0.3)
	ax.set_xlabel('Site')
	ax.set_ylabel('Measured Noise (dB)')
	ax.set_title(plot_title)
	ax.set_ylim([30,90])

	# The IDOT abatement approach value
	IDOT_approach_db = 66
	ax.axhline(y=IDOT_approach_db, color="red")
	ax.text(-3,66, "{:.0f} db".format(IDOT_approach_db), color="red",ha="left", va="bottom")
	# From: https://stackoverflow.com/questions/42877747/add-a-label-to-y-axis-to-show-the-value-of-y-for-a-horizontal-line-in-matplotlib
	return 0

def build_traffic_lookup_dict(df):
	northbound_column = 'Northbound Traffic'
	southbound_column = 'Southbound Traffic'
	
	traffic_lookup_dict = {}
	for code in set(df['Full Code']):
		site_time_traffic_dict = {}
		site_time_traffic_dict[northbound_column] = df.loc[df['Full Code']==code][northbound_column].iloc[0] # use the first result of 3 - they look like all are the same for each data collect.
		site_time_traffic_dict[southbound_column] = df.loc[df['Full Code']==code][southbound_column].iloc[0] # use the first result of 3 - they look like all are the same for each data collect.
		traffic_lookup_dict[code] = site_time_traffic_dict

	return traffic_lookup_dict

def bar_site_at_different_times(site_string, max_log_means, traffic_lookup_dict, time_codes = ['X','A','B','C']):
	# Adding grouping by quality
	site_time_groupby = max_log_means.groupby(['Site Code','Time Code'])
	#site_time_groupby.get_group(('BTD','good'))[x_column]
	
	# Initializations for plotting:
	fig, ax = plt.subplots(figsize=(9, 6))
	width = 10
	multiplier = 1.1
	i_bar = 0
	label_pos = []
	bar_labels = []
	traffic_color_lookup = {'BTD':'tab:blue', 'GREEN':'tab:green', 'ORANGE':'tab:orange', 'RED':'tab:red','DARK RED':'tab:brown'}
	
	
	for i in range(len(time_codes)):
		i_bar = i_bar + 1
		offset = width * multiplier
		x = i_bar + offset
		
		measurement = site_time_groupby.get_group((site_string,time_codes[i]))['Max Log Mean (dB)'].iloc[0]

		bar_label = time_codes[i]
		bar_labels.append(bar_label)
		label_pos.append(x)
		
		#the_bar = ax.bar(x, round(measurement), width, label=bar_label,color='tab:blue') # dang you want to color by traffic again don't you!?
		#ax.bar_label(the_bar, padding=3)
		
		if time_codes[i] == 'X':
			the_bar = ax.bar(x, round(measurement), width, label=bar_label,color='tab:blue') # dang you want to color by traffic again don't you!?
			ax.bar_label(the_bar, padding=3)
			
		else:
			nobo_traffic = traffic_lookup_dict[max_log_means['Full Code'].iloc[i]]['Northbound Traffic']
			sobo_traffic = traffic_lookup_dict[max_log_means['Full Code'].iloc[i]]['Southbound Traffic']
			nobo_traffic_color = traffic_color_lookup[nobo_traffic]
			sobo_traffic_color = traffic_color_lookup[sobo_traffic]
			
			the_bar0 = ax.bar(x, 0, width, label=bar_label,color='tab:blue') # just for the label
			x1 = i_bar + offset - 0.25*width
			x2 = i_bar + offset + 0.25*width
			the_bar = ax.bar(x1, round(measurement), width/2, label=bar_label,color=sobo_traffic_color) # southbound on the left b/c 'MERICA!
			the_bar2 = ax.bar(x2, round(measurement), width/2, label=bar_label,color=nobo_traffic_color)
			ax.bar_label(the_bar0, padding=3)
		
		multiplier += 1

	# Adjustments to plotting area
	ax.set_xticks(label_pos, labels=bar_labels)
	plt.subplots_adjust(bottom=0.3)
	ax.set_xlabel('Site')
	ax.set_ylabel('Measured Noise (dB)')
	ax.set_title(site_string)
	ax.set_ylim([30,90])
	
	# The IDOT abatement approach value
	IDOT_approach_db = 66
	ax.axhline(y=IDOT_approach_db, color="red")
	ax.text(5,66, "{:.0f} db".format(IDOT_approach_db), color="red",ha="left", va="bottom")
	# From: https://stackoverflow.com/questions/42877747/add-a-label-to-y-axis-to-show-the-value-of-y-for-a-horizontal-line-in-matplotlib
	
	return 0

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


df = loading.load_calc_data(data_path,file_list)
df = loading.filter_sites_by_distance(df) # verified that it worked.
traffic_lookup_dict = build_traffic_lookup_dict(df)
df = df.reset_index(drop=True)

#noise_vs_distance_plot(df)
#noise_vs_distance_plot_with_redline(df)
#lognoise_vs_distance_plot_with_redline(df) # helps a bit? very small difference

# Forget distance, use a bar graph. Add stdev to the plot (or don't):
# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py

# Not a valid plot, but things seem to be working.
max_log_means = analysis.collection_high_stat(df,'Log Mean (dB)')
max_log_means.to_csv('GAAA.csv')
max_log_means = analysis.take_larger_location_meas(max_log_means,'Max Log Mean (dB)')
print(max_log_means)
max_log_means.to_csv('max_log_means.csv')
print(max_log_means.values.shape)
"""
fig, ax = plt.subplots(figsize=(18, 6))
max_time_code_groups = max_log_means.groupby(['Time Code'])
ax.plot(max_time_code_groups.get_group('X')['Max Log Mean (dB)'],marker='^', c='b', label='BTD')
ax.plot(max_time_code_groups.get_group('A')['Max Log Mean (dB)'],marker='o', c='r', label='A')
ax.plot(max_time_code_groups.get_group('B')['Max Log Mean (dB)'],marker='o', c='k', label='B')
ax.plot(max_time_code_groups.get_group('C')['Max Log Mean (dB)'],marker='o', c='m', label='C')
plt.show()
"""

# Plot all the data from all of the sites: max log means
#bar_plot_by_time_code(max_log_means)
time_code_groups = max_log_means.groupby('Time Code')
#bar_plot_by_time_code(time_code_groups.get_group('X'), 'Bike The Drive')
#bar_plot_by_time_code(time_code_groups.get_group('A'), 'Time A') # two collections at 9-14 and 9-16 hmmmm
#bar_plot_by_time_code(time_code_groups.get_group('B'), 'Time B') # two collections at 9-14 and 9-16 hmmmm
#bar_plot_by_time_code(time_code_groups.get_group('C'), 'Time C')

# MONEY PLOTS! YES!
time_code_traffic_bar(time_code_groups.get_group('X'), 'BTD',traffic_lookup_dict)
time_code_traffic_bar(time_code_groups.get_group('A'), 'Time A',traffic_lookup_dict)
time_code_traffic_bar(time_code_groups.get_group('B'), 'Time B',traffic_lookup_dict)
time_code_traffic_bar(time_code_groups.get_group('C'), 'Time C',traffic_lookup_dict)
# N is very impacted by the traffic noise
# Z is heavily impacted
# S was even loud during bike the drive (water feature + wind in wide open spaces? Explain this somehow.)


# Compare different sites at different times:
# Look at dramatic effects, things like playgrounds and places where people will linger.
bar_site_at_different_times('N-01-101',max_log_means,traffic_lookup_dict,['X','A','B','C'])
bar_site_at_different_times('S-02-101',max_log_means,traffic_lookup_dict,['X','A','B','C'])
bar_site_at_different_times('Z-01-101',max_log_means,traffic_lookup_dict,['X','A','B','C'])
bar_site_at_different_times('Z-02-101',max_log_means,traffic_lookup_dict,['X','A','B','C'])


# LAST PLOT: demonstrate decreasing noise with increasing traffic
# How about a scatter plot of noise vs BTD, GREEN, ORANGE, RED, etc.


# PLAN A
# Show tons of little bars for log mean average for all collection runs, shaded bar in background averages the averages

# Do for individual sites, x axis is time code.
# PLAN B
# Show line plots of all the data runs (something to try in any event)

# PLAN C
# Combine A and B? OH ALL THE TIME I COULD SPEND HERE!

# DON'T FORGET TO CHANGE THE MAX LOG MEAN TERMINOLOGY
# Hourly equivalent noise level (does the manual explain this? Make sure you calculate the correct one the correct way)
# dB (A), not dB (understand this)
# 

plt.show()



