#coding=utf8
'''
Anna Bonazzi, 15/08/2017

Script to get ngrams (sentence units / word chains) of desired length from a corpus. 
Makes ngrams for different corpus sections (in this case, corpus is divided by class and language), returns absolute frequency and frequency per million.

Option 1) uses nltk (respects capitalization, accepts 1 ngram length only)
Option 2) uses scikit-learn (doesn't respect capitalization, accepts a min and max ngram length window. Currently commented out).

('.decode('utf-8')' mess necessary for python 2.7, not for python 3)

Basic structure:
text = 'In a hole in the ground there lived a hobbit'
ngram_lenght = 3
searchword = 'hobbit' # Optional
grams = ngrams(text.split(), ngram_length)
sorted_ngrams = {}
for g in grams:
	try:
		if searchword in g:
			if g in sorted_ngrams:
				sorted_ngrams[g] += 1
			else:
				sorted_ngrams[g] = 1
	except:
		if g in sorted_ngrams:
			sorted_ngrams[g] += 1
		else:
			sorted_ngrams[g] = 1
# Sorts by frequency
sorted_tuples = sorted(sorted_ngrams.items(), key=lambda pair: pair[1], reverse=True)
with open (output_file, 'a') as out:
	for tup in sorted_tuples:
		out.write(tup)
'''
#------------------------------
# VARIABLES FOR USER TO CHANGE

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/folder/'

langs = ['it', 'de', 'fr', 'en']
unit = 'wordform' # Options: 'wordform', 'pos', 'lemma'
n = 3 # Ngram window with nltk
min_ = 5; max_ = 5 # Ngram window with sci-kit learn

min_freq = 2 # Minimum ngram frequency
max_number = 500 # Number of ngrams to show

#searchword = 'hobbit' # Comment out if not needed
#------------------------------

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk import ngrams
import re
# To time the script
from datetime import datetime
startTime = datetime.now()

# 1) With nltk (slightly slower, more accurate)

for lang in langs:	
	print ('\nSearching in language '+lang.title()) 
	pab = [] ; pbv = []; peb = []; pfu = []					
	chunk = [] # Prepares temporary text as list		
	counter = 0
	units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2}
	# Goes through corpus
	with open (input_file, 'r') as f:
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					chunk.append(line.split("\t")[units[unit]])#.decode('utf-8'))
				elif '<text' in line or '</s' in line:
					chunk.append(line)
				
			else: # Meets text end, works on temporary text chunk
				chunk.append(line)#.decode('utf-8'))
			  	# Searches for chosen lang/class combination
				regex = re.search('class="(.*?)".*?language="'+lang+'"', ''.join(chunk))
				if regex:
					cl = regex.group(1)
					for word in chunk:
						if '<text' not in word and '</text' not in word:
							if cl == 'pab':
								pab.append(word)
							elif cl == 'pbv':
								pbv.append(word)
							elif cl == 'peb':
								peb.append(word)
							elif cl == 'pfu':
								pfu.append(word)
				chunk = []
				counter += 1
				if '00000' in str(counter):
					print ("\tText " + str(counter))

	texts = []
	def prepare_text(dic, cl):
		# Text are tuples of 1) text and 2) class label
		text = (' '.join(dic), cl)
		texts.append(text) 

	prepare_text(pab, 'pab') ; prepare_text(pbv, 'pbv') ; prepare_text(peb, 'peb') ; prepare_text(pfu, 'pfu')

	print ('Now making ngrams')
	for text in texts:	# For every class	
		# Makes ngrams
		grams = ngrams(text[0].split(), n)
		sorted_ngrams = {}
		tot_grams = 0
		for g in grams:
			tot_grams += 1
			try:
				if '</s>' not in g and searchword in g: # If searchword is given
					if g in sorted_ngrams:
						sorted_ngrams[g] += 1
					else:
						sorted_ngrams[g] = 1
			except:
				if '</s>' not in g: # Respects sentence boundary
					if g in sorted_ngrams:
						sorted_ngrams[g] += 1
					else:
						sorted_ngrams[g] = 1

		sorted_tuples = sorted(sorted_ngrams.items(), key=lambda pair: pair[1], reverse=True)
		count = 0
		with open (output_folder + str(n)+'-grams_'+lang+'_'+text[1]+'_'+unit+'.txt', 'a') as out:
			for tup in sorted_tuples:
				if tup[1] >= min_freq and count <= max_number and '</s>' not in tup[0]:
					count += 1
					# Counts frequency per million 
					pmi = float('{:.2f}'.format(int(tup[1]) * 1000000 / tot_grams))
					if n == 5:
						out.write(str(pmi) + '\t' + str(tup[1]) + '\t' + str(tup[0][0]) + '\t' + str(tup[0][1]) + '\t' + str(tup[0][2]) + '\t' + str(tup[0][3]) + '\t' + str(tup[0][4]) +'\n')
					elif n == 3:
						out.write(str(pmi) + '\t' + str(tup[1]) + '\t' + str(tup[0][0]) + '\t' + str(tup[0][1]) + '\t' + str(tup[0][2]) +'\n')
					else:
						out.write(str(pmi) + '\t' + str(tup) +'\n')
					
	sorted_tuples = {}
				

# 2) With sci-kit learn (faster, less precise, no capital letters)
'''
vect = CountVectorizer(ngram_range=(min_,max_)) 
# (1,4: everything from 1-gram to 4-gram. 4,4: only 4-grams)

analyzer = vect.build_analyzer()
ngram_list_temp = analyzer(text)
ngram_list_temp.reverse()

searchword = searchword.lower()
ngrams = {}
for ngram in ngram_list_temp:
	if searchword in ngram and '</s' not in ngram: # searchword.decode('utf-8')
		if ngram in ngrams:
			ngrams[ngram] += 1
		else:
			ngrams[ngram] = 1

# Sorts, prints out
sorted_tuples = sorted(ngrams.items(), key=lambda pair: pair[1], reverse=False) # False: rare to frequent / True: frequent to rare
for tup in sorted_tuples:
	if tup[1] >= min_freq:
		print (str(tup[1]) + '\t' + str(tup[0].encode('utf-8')) + "\n")
'''

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
