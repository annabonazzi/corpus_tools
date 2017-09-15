# coding=utf8
'''
Anna Bonazzi, 02/08/17
Script to clean a wordlist of words mixed with numbers (clean all lists or pick only specific lines)
'''
#---------------------
# VARIABLES FOR USER TO CHANGE
input = '/home/bonz/Documents/Corpus_work/GEothermie2020/frequenz/freq_en.txt'
output = '/home/bonz/Documents/Corpus_work/GEothermie2020/frequenz/freq_en2.txt'
#---------------------
import re
dic = {}
with open (input, 'r') as f:
	# Takes part of all lines
	words = f.readlines()
	for word in words:
		with open (output, 'a') as o:
			word.replace('\t', ' ')
			o.write(word.split(' ')[0] + '\t' + word.split(' ')[1] + '\n')
	'''
	#---------------
	# Picks/avoids specific lines
		regex = re.search("\d.*?\t\d", word)
		if regex:
			pass
		else:
			print word
			with open (output, 'w') as out:
				out.write(word + '\n')
  '''
print ('Done!\n')
