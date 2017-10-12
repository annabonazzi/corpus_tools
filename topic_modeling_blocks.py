#coding=utf8
'''
Anna Bonazzi, 14/09/2017

Script to model document topics with LDA (Latent Dirichlet Allocation). Sample script assembled from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

Texts are assembled from a corpus based on certain features and then modeled.

Works only for python2 (gensim currently unavailable for python3))
'''
# VARIABLES FOR USER TO CHANGE

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/topics_folder/'
topic_number = 200
words_per_topic = 8
min_freq = 10 # Minimum acceptable word frequency (rare words are ignored)
top_percent = 5 # Percentage of words to be skipped (too frequent)
bottom_percent = 10 # Percentage of words to be skipped (too rare)
lang = 'fr'
#---------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re, nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim (only python 2! .decode('utf-8'))
# if python3: install with "pip2 install gensim", then run script with "python2 script.py"
import gensim
from gensim import corpora
#---------------------------

# 1) Prepares text to be modeled as list of strings
flag = 0
fhandle = open (output_folder+lang+'_topics-'+str(topic_number)+'-'+str(words_per_topic)+'_min-'+str(min_freq)+'_cut-'+str(top_percent)+'-'+str(bottom_percent)+'.txt', 'a')
print ('Going through corpus. Go have a coffee.\n')
text_counter = 0
counter = 0
doc = []
docs = []
chunk = []
with open (input_file, 'r') as f:	
	for line in f:
		if '</text>' not in line: # Works text by text
			if '<' not in line:
				# Lemmas [2], wordforms [0], pos [1]
				chunk.append(line.split("\t")[2].decode('utf-8'))
			elif '<text' in line:
				chunk.append(line.decode('utf-8'))
		else: # Meets text end, works on temporary text chunk
			text_counter += 1
			chunk.append(line.decode('utf-8'))
		  	# Searches for chosen lang/class combination
			regex = re.search('language="'+lang+'".*?subclass=".*?".*?', ''.join(chunk))
			if regex:
				for word in chunk:
					if '<' not in word and '@card@' not in word and '©'.decode('utf-8') not in word and 'être'.decode('utf-8') not in word:
						doc.append(word)
				docs.append(' '.join(doc))
			chunk = []
			doc = []
			if '00000' in str(text_counter):
				print (str(text_counter))
if len(docs) < 1:
	flag = 1 # Skips topic modeling if the class is empty		

'''
# Groups single doc strings into strings of 1000 docs each
new_docs = []
for i in range(0, len(docs), 1000): 
	new_docs.append(' '.join(docs[i:i + 1000]))
docs = []; docs = new_docs; new_docs = []
'''
#-------------------------
# 2) Starts topic modeling
if flag == 0:
	print ('Starting topic modeling')
	# Cleaning and preprocessing
	langs = {'fr' : 'french', 'de' : 'german', 'it' : 'italian', 'en' : 'english'}
	stop = set(stopwords.words(langs[lang]) + ['avoir', 'e', 'aucun']) # Also add custom "useless" words, such as stop = stopwords.words('english') + ['rt', 'via']
	punct = set(string.punctuation)
	lemma = WordNetLemmatizer()
	def clean(doc):
		word_count = {}
		all_words = 0
		for word in doc.split(' '): # Prepares to skip words with low freq
			all_words += 1
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
		# word : tot = x : 100
		sorted_tuples = sorted(word_count.items(), key=lambda pair: pair[1], reverse=True)
		# Calculates percentage bins
		x = int(str(float("{:.5f}".format(len(sorted_tuples) / 100))).split('.')[0])
		# Creates list of numbers that represent an acceptable frequency (not too high or too low index)
		i_max = x*top_percent; i_min = -(x*bottom_percent)
		selected_tup = []
		# Selects acceptable frequencies
		selected_tup = sorted_tuples[i_max:i_min]	
		sorted_tuples = []
		selected_freq = []
		for tup in selected_tup:
			selected_freq.append(tup[1])
		# Splits and reassembles text without super rare/frequent words
		rare_free = ' '.join([word for word in doc.split(' ') if word_count[word] in selected_freq and word_count[word] > min_freq])
		# Splits and reassemples text without stopwords
		stop_free = ' '.join([word for word in doc.lower().split(' ') if word not in stop])
		# Splits and reassembles text without punctuation
		punc_free = ''.join(ch for ch in stop_free if ch not in punct)
		#normalized = ' '.join(lemma.lemmatize(word) for word in punc_free.split())
		return punc_free # return normalized

	doc_clean = [clean(doc).split() for doc in docs] # List of wordlists
	
	# Preparing Document-Term Matrix

	# Creating the term dictionary of our courpus, where every unique term is assigned an index. 

	dictionary = corpora.Dictionary(doc_clean)

	# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
	doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

	# Running LDA Model

	# Creating the object for LDA model using gensim library
	Lda = gensim.models.ldamodel.LdaModel

	# Running and Trainign LDA model on the document term matrix.
	ldamodel = Lda(doc_term_matrix, num_topics=topic_number, id2word = dictionary, passes=50)
	# Results
	results = (ldamodel.print_topics(num_topics=topic_number, num_words=words_per_topic))

	for r in results:
		print ('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + ')).encode('utf-8')))
		fhandle.write('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + ')).encode('utf-8')) + '\n\n')
	fhandle.close()
	results = []
	doc_term_matrix = []
	dictionary = None
	Lda = None
	ldamodel = None
	doc_clean = []
	# New document starts

#--------------------------
# To time the script
time = datetime.now() - startTime

print ("\n(Script running time: " + str(time) + ")")
