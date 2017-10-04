#!/usr/bin/python3
#coding=utf8
'''
Anna Bonazzi, 06/09/2017

Script to find collocates of specific words from a corpus.

What the script does:
	1) Picks corpus texts with chosen language, puts them together as word list
	2) Finds collocations (basis-collocate pairs) in window of given size
	3) Selects collocations containing the desired searchword or basis
	4) Sorts the searchword's collocates by log-likelihood or pmi value

! Requires all the encode/decode mess in python2.7. Comment it out for python 3.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

searchwords = ['association', 'club']
lang = 'fr'
#languages = ['fr', 'de'] # For list of languages, make one more "for" loop

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/collocates_folder/'

min_freq = 3 # Minimum collocation frequency to be considered
window_size = 6 # Size of word window to search for collocates
unit = 'lemma' # Options: 'lemma', 'wordform', 'pos'
coll_measure = 'likelihood_ratio' # Options: 'likelihood_ratio', 'pmi'
#---------------------

# To time the script
from datetime import datetime
startTime = datetime.now()

import os, glob, re, sys
# If needed: first run "sudo pip install nltk"
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *
# To recognize punctuation
import string
#---------------------

# Prepares to removes punctuation
punct = set(string.punctuation + '»' + '«')
# 1) Assembles text with chosen lang combination
for sw in searchwords:
	print ('!! Now searching collocates of "' + sw +'"')
	text_counter = 0 # To keep track
	chunk = [] # Prepares temporary text as list
	text = []
	sw_freq = 0
	flag = 0 # To skip collocation making with irrelevant texts
	# Goes through corpus
	with open (input_file, 'r') as f:
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2} 
					chunk.append(line.split("\t")[units[unit]].decode('utf-8'))
				elif '<text' in line:
					chunk.append(line)
				elif '</s' in line:
					chunk.append(line.strip('\n'))
		
			else: # Meets current text end
				chunk.append(line.decode('utf-8'))
			  	# Searches for chosen lang combination
				regex = re.search('class="(.*?)".*?language="'+lang, ''.join(chunk))
				if regex:
					for word in chunk:
						if '</s' in word:
							text.append(word)
						if '<' not in word and word not in punct: # Excludes xml and punctuation
							text.append(word) # Saves text with right properties as list
						if word == sw or word == sw.lower():
							sw_freq += 1
											
					text_counter += 1
				if '00000' in str(text_counter):
					print ("\tText " + str(text_counter))
				chunk = [] # Resets empty chunk for next corpus text

	# text is now a list
	if sw not in text or sw.lower() not in text:
		#sys.exit("\nSearchword " + sw + " not in corpus.\n")
		print ("\nSearchword " + sw + " not in corpus.\n")
		flag = 1
	else:
		print ("Searchword " + sw + " is there " + str(sw_freq) + " times")

#----------------------------------------	
	if flag == 0:
	# 2) Makes collocations
		time1 = datetime.now() - startTime
		print ('Making collocations after ' + str(time1) + '\n')	
		
		# Prepares text (list or string) in nltk format

		corpus = nltk.Text(text) # From list
		#corpus = nltk.wordpunct_tokenize(text) # From string
		text = None

		# Makes 2-/3-grams with PMI or log-likelihood values and given window size
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		bi_finder = BigramCollocationFinder.from_words(corpus, window_size = window_size)

		# Filters ngrams by frequency
		bi_finder.apply_freq_filter(min_freq)
		# Filters ngrams by searchword
		my_filter = lambda *w: sw not in w and sw.lower() not in w
		bi_finder.apply_ngram_filter(my_filter)
		# Filters ngrams with sentence boundary
		my_filter = lambda *w: '</s>' in w
		bi_finder.apply_ngram_filter(my_filter)
		# Makes collocations
		if coll_measure == 'likelihood_ratio':
			bi_list = bi_finder.score_ngrams(bigram_measures.likelihood_ratio)
		else:
			bi_list = bi_finder.score_ngrams(bigram_measures.pmi)
	
	#----------------------------------------	
	# 3) Sorts collocates by their log-lik or pmi value
		collocates = {}
		# Prepares to remove stopwords
		pairs = {'de' : 'german', 'fr' : 'french', 'en' : 'english', 'it' : 'italian'}
		stop = set(stopwords.words(pairs[lang]) + ['L', 'l', '’', 'être', 'card', 'avoir', '@card@', 'S', '’', '@ord@'])
		# Collocation format: ((word1, word2), (log-l-value))
		
		for coll in bi_list:
			for word in coll[0]:
				if not word == sw and not word == sw.lower() and word not in stop:
					if word not in collocates:
						collocates[word] = coll[1]

		# Sorts and prints out
		sorted_tuples = sorted(collocates.items(), key=lambda pair: pair[1], reverse=True)
		for tup in sorted_tuples:
			print(str('{0:.4f}'.format(tup[1])) + '\t' + str(tup[0].encode('utf-8')) + '\n')
		'''
		with open (output_folder + lang + '_' + sw + '.txt', 'a') as out:
			for tup in sorted_tuples:
				out.write(str('{0:.4f}'.format(tup[1])) + '\t' + str(tup[0]) + '\n') # tup[0].encode('utf-8')
		'''
		collocates = {} # Resets

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
