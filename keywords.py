#coding=utf8
'''
Anna Bonazzi, 06/10/2017

Script to extract corpus keywords with log-likelihood test through a comparison with another corpus

Current settings for python3. Additional ".decode('utf-8')" on strings required for python2.7 (currently there but commented out, uncomment if needed).
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE

corpus1 = '/path/to/corpus1.vrt' # Interesting corpus
corpus2 = '/path/to/corpus2.vrt' # Big comparison corpus
output_folder = '/path/to/keywords_folder/'
min_freq = 10 # Minimum frequency of keyword candidates
lang = 'fr' # Pick language from multilingual corpus
unit = 'wordform' # Options: 'wordform', 'lemma', 'pos'
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
import numpy as np #np.log is ln; np.log10 = log
from nltk.corpus import stopwords
#--------------------------
# Prepares to remove stopwords
langs = {'fr' : 'french', 'de' : 'german', 'it' : 'italian', 'en' : 'english'}
stop = set(stopwords.words(langs[lang]) + ['avoir', 'e', 'aucun', '»', '«', '@card@', '<', '©', 'être', 'Les', 'les']) #.decode('utf-8')

# Extracts text with chosen properties from corpus
def text_from_corpus(corpus):
	print ('Searching '+corpus+'... patience.')
	word_tot = 0
	word_dic = {}
	text_counter = 0
	chunk = []
	with open (corpus, 'r') as f:	
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					units = {'wordform' : 0, 'lemma':2, 'pos':1}
					word = line.split("\t")[units[unit]]#.decode('utf-8'))
					# Lemmas [2], wordforms [0], pos [1]
					chunk.append(word)						
				elif '<text' in line:
					chunk.append(line)#.decode('utf-8'))
			else: # Meets text end, works on temporary text chunk
				text_counter += 1
				chunk.append(line)#.decode('utf-8'))
				
			  	# Looks for chosen text attribute combinations
				regex = re.search('language="'+lang+'".*?subclass=".*?".*?', ''.join(chunk))
				if regex:
					for word in chunk:
						if '<text' not in word.split(' ') and word not in stop:
							# Counts total words and frequency of each word
							word_tot += 1
							if word in word_dic:
								word_dic[word] += 1
							else:
								word_dic[word] = 1
				chunk = []
				doc = []
				if '00000' in str(text_counter):
					print (str(text_counter))
		return (word_tot, word_dic)

word_tot1, word_dic1 = text_from_corpus(corpus1)
word_tot2, word_dic2 = text_from_corpus(corpus2)

keywords = {} # For statistically significant keywords
all_keywords = {} # For all keywords in order

# Values needed for log-likelihood test: observed and expected freq of each word
for word in word_dic1:
	if word_dic1[word] >= min_freq:
		if word not in word_dic2:
			word_dic2[word] = 0.1
		#  Expexted freq: e1 = c*(a+b) / (c+d), e2 = d*(a+b) / (c+d)
		e1 = float(word_tot1 * (word_dic1[word] + word_dic2[word]) / (word_tot1 + word_tot1))
		e2 = float(word_tot2 * (word_dic1[word] + word_dic2[word]) / (word_tot1 + word_tot1))
		# Log-lik = 2*((a*ln (a/E1)) + (b*ln (b/E2)))
		loglik = 2 * ((word_dic1[word] * np.log(word_dic1[word]/e1)) + (word_dic2[word] * np.log(word_dic2[word]/e2)))
		if loglik >= 3.8:
			keywords[word] = loglik
		else:
			all_keywords[word] = loglik

sorted_tuples = sorted(keywords.items(), key=lambda pair: pair[1], reverse=True)
# (tup[0].encode('utf-8')), (tup[1]).encode('utf-8')

with open (output_folder+lang+'_significant.txt', 'a') as out:
	for tup in sorted_tuples:
		print (str(tup[1]) + "\t" + str(tup[0]) + "\n")
		out.write(str(tup[0]) + "\t" + str(tup[1]) + "\n")

sorted_tuples = sorted(all_keywords.items(), key=lambda pair: pair[1], reverse=True)
with open (output_folder+lang+'_all.txt', 'a') as out:
	for tup in sorted_tuples:
		out.write(str(tup[0]) + "\t" + str(tup[1]) + "\n")
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
