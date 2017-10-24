#coding=utf8
'''
Anna Bonazzi, 06/09/2017

Script to group corpus actors based on their use of collocations. 
Requires predefined collocation profiles (see line 32) in this format:
	'economic field' : ['expensive', 'debit', 'money'], 'political field' : ['president', 'parliament', 'laws'], etc... 

What the script does:
	1) Picks corpus texts with chosen language and containing searchword. 
	2) Looks for text chunks (ngrams of given size) where the searchword is.
	3) Counts the frequency of every collocate for every profile. Sums them to obtain the global profile value for each source.
	4) Counts relative frequency of profile words (% of the frequency of searchword in that source)
	5) Represents results as table where rows are sources and columns are profiles.

Current settings for python 2.7 (for python 3, comment all the ".decode('utf-8')" out).
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

searchword = 'géothermie'
reg = 'géotherm.*' # Upper case / Lower case will be fixed later
coll_profiles = {'Energieressource' : ['biomasse', 'solaire', 'hydraulique', 'éolien', '’eau', 'photovoltaïque', '^gaz', '^thermique', 'hydro-thermique', 'biogaz', 'bois'], 
'Grüne Energie' : ['biomasse', 'solaire', 'hydraulique', 'éolien', '’eau', 'photovoltaïque', 'gaz', 'chaleur'], 
'Energiewirtschaft' : ['prospection', 'exploitation', 'utilisation', 'production', 'exploiter']}

lang = 'fr'

input_file = '/path/to/corpus_file.vrt'
output_folder = 'path/to/collocates_folder/'
window_size = 6 # Size of word window to search for collocates
unit = 'lemma' # Use lemma if the collocates were obtained as lemmas, or wordform if collocates are wordforms
#---------------------

# To time the script
from datetime import datetime
startTime = datetime.now()
import pandas as pd
import os, glob, re, sys
#---------------------

# 1) Looks for texts with chosen language containing the searchword
			
chunk = []
sources = {}; sources_percent = {}
sw_counter = {}
text_counter = 0
switch = 0
reg = reg.decode('utf-8')
print('Collecting collocate frequency info. Hold on...')
with open (input_file, 'r') as f:
	for line in f:
		if '</text>' not in line: # Works text by text
			if '<' not in line:
				units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2} 
				chunk.append(line.split("\t")[units[unit]].decode('utf-8'))
			elif '<text' in line:
				chunk.append(line.decode('utf-8'))
			elif '</s' in line:
				chunk.append(line.strip('\n').decode('utf-8'))
	
		else: # Meets current text end
			# Checks text for chosen properties (language and basis)
			regex = re.search('(?i)class=".*?".*?language="'+lang+'".*?source="(.*?)".*?\n.*?'+reg, ' '.join(chunk))
			if regex:
				source = regex.group(1)
				if source not in sources:
					sources[source] = {}
				
				switch = 1
				chunk = chunk[1:]
				temp = []
				for word in chunk:						
					# Saves only ngrams where word is, shifting 1 by 1
					while len(temp) < window_size:
						temp.append(word)
					if len(temp) == window_size:
						# Skips ngrams that have sentence break
						if '</s' not in ' '.join(temp):
							basis = re.search(reg, ' '.join(temp))
							if basis:
								# Saves frequency of searchword (multiplied in many ngrams - not real, but useful as proportion)
								if source in sw_counter:
									sw_counter[source] += 1
								else:
									sw_counter[source] = 1
								# Checks every profile
								for profile in coll_profiles:
									if profile not in sources[source]:
										sources[source][profile] = 0
									# Checks for every collocate in profile
									for coll in coll_profiles[profile]:
										collocate = re.search('(?i)'+coll.decode('utf-8'), ' '.join(temp))
										if collocate:
											# Saves frequency of profile elements (multiplied in many ngrams - not real, but useful as proportion)
											sources[source][profile] += 1									
										
						# Continues shifting right with new ngrams					
						temp.pop(0)
					else:
						temp.pop(0)
				
			chunk = []
			text_counter += 1
			if '0000' in str(text_counter):
				print(text_counter)

if switch == 0:
	print('Word is not there')
else:
	# Complete empty table rows 
	for source in sources:
		sources_percent[source] = {}
		print(source + ' ' + str(sw_counter[source]))
		for profile in coll_profiles:
			# Makes parallel dictionary with relative frequency
			if sources[source][profile] > 0:
				rel_freq = float('{:.2f}'.format(float(sources[source][profile]) * 100 / sw_counter[source]))
				sources_percent[source][profile] = rel_freq
			else:
				sources_percent[source][profile] = 0
	
	# Puts results into a table
	df = pd.DataFrame.from_dict(sources)
	df = df.T # Swaps x and y
	
	df_percent = pd.DataFrame.from_dict(sources_percent)
	df_percent = df_percent.T # Swaps x and y

	# Sums all column values, adds row with column sum
	for cl in coll_profiles.keys():
		df.at['Profilrelevanz', cl] = df[cl].sum()
		df_percent.at['Profilrelevanz', cl] = df_percent[cl].sum()
	
	# Sums all row values, adds row with row sum
	row_sum = df.sum(axis=1) # Type: series
	df['Thematische Dichte'] = row_sum # Takes list or pandas series

	row_sum = df_percent.sum(axis=1)
	df_percent['Thematische Dichte'] = row_sum

	#print(df_percent)
	
	df.to_csv(output_folder+searchword+'_profiles3.csv', sep='\t')
	df_percent.to_csv(output_folder+searchword+'_profiles_percent3.csv', sep='\t')
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
