#coding=utf8
'''
Anna Bonazzi, 10/08/17

Script to extract specific texts from a corpus and make a separate smaller corpus file.
Selected sources are given through their short name as found in the <text> line of each corpus text.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE

corpus = '/path/to/corpus_file.vrt'
new_subcorpus = '/path/to/subkorpus_file.vrt'
selected_sources = '/path/to/selected_sources_list.txt'
# OR
#sources = ['20min', 'tribune']
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
#--------------------------

# Reads subcorpus source names from file into a list
try:
	with open (selected_sources, 'r') as f:
		sources = f.readlines()
	for i in range (0,len(sources)):
		sources[i] = sources[i].strip('\n')
except:
	pass

# Prepares subcorpus file where to copy texts
fhandle = open (new_subcorpus, 'a')
fhandle.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n')<corpus>\n') # Adjust for corpus format

chunk = []
counter = 0		  
# Opens corpus
with open (corpus, 'r') as f: # Reads only line by line, doesn't save all
	for line in f:
		if '</text>' not in line:
			chunk.append(line) # Fills chunk 
		else: # Meets text end
			chunk.append(line)
			# Searches for selected source names
			regex = re.search('source="(.*?)"', ''.join(chunk))
			if regex:
				source = regex.group(1)
				if source in sources:
					counter += 1
					if '0000' in str(counter):
						print (str(counter))
					fhandle.write(''.join(chunk))
			chunk = [] # resets empty list
			# Starts accumulating lines again until next text-end
	
fhandle.write('</corpus>')
fhandle.close()		
		 
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
