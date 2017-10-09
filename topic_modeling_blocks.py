#coding=utf8
'''
# Anna Bonazzi, 14/09/2017
Script to model document topics with LDA (Latent Dirichlet Allocation). Sample script assembled from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

The script extracts texts with chosen attributes from the corpus and analyzes them in blocks of chosen length
'''
# VARIABLES FOR USER TO CHANGE

input_file = '/home/bonz/Documents/Corpora/geothermie.vrt'
output_folder = '/home/bonz/Documents/Corpus_work/GEothermie2020/topics/'
lang = 'fr'
topic_number = 300
words_per_topic = 6
text_block = 100000

#---------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re, nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim (only python 2! .decode('utf-8'))
# If python3: install with "pip2 install gensim", then run script with "python2.7 script.py"
import gensim
from gensim import corpora
#---------------------------

# 1) Prepares text to be modeled as list of strings
flag = 0
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
				chunk.append(line.split("\t")[2])#.decode('utf-8'))
			elif '<text' in line:
				chunk.append(line)#.decode('utf-8'))
		else: # Meets text end, works on temporary text chunk
			text_counter += 1
			chunk.append(line)#.decode('utf-8'))
		  	# Searches for chosen lang/class combination
			regex = re.search('language="'+lang+'".*?subclass=".*?".*?', ''.join(chunk))
			if regex:
				for word in chunk:
					if '<' not in word and '@card@' not in word and '©' not in word and 'être' not in word: # .decode for strange words
						doc.append(word)
				docs.append(' '.join(doc))
			chunk = []
			doc = []
			if '00000' in str(text_counter):
				print (str(text_counter))	

# Groups single doc strings into strings of 1000 docs each
group = []
for i in range(0, len(docs), text_block): 
	group = docs[i:i + text_block]
	fhandle = open (output_folder+str(i + text_block)+'_'+lang+'_topics-'+str(topic_number)+'-'+str(words_per_topic)+'-'+str(text_block)+'-pro-block_no-rare.txt', 'a')
#-------------------------
# 2) Starts topic modeling

	print ('Starting topic modeling')
	# Cleaning and preprocessing
	langs = {'fr' : 'french', 'de' : 'german', 'it' : 'italian', 'en' : 'english'}
	stop = set(stopwords.words(langs[lang]) + ['avoir', 'e', 'aucun']) # Also add custom "useless" words, such as stop = stopwords.words('english') + ['rt', 'via']
	exclude = set(string.punctuation)
	lemma = WordNetLemmatizer()
	def clean(doc):
		word_count = {}
		for word in doc.split(' '):
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
		stop_free = " ".join([word for word in doc.lower().split(' ') if word not in stop and word_count[word] > 2])
		punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
		normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
		return normalized

	doc_clean = [clean(doc).split() for doc in group] # List of wordlists
	
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
		print ('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + ')))) # join().encode('utf-8')
		fhandle.write('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + '))) + '\n\n') # join().encode('utf-8')
	fhandle.close()
	results = []
	doc_term_matrix = []
	dictionary = None
	Lda = None
	ldamodel = None
	doc_clean = []
	group = []
	# New documents group starts

#--------------------------
# To time the script
time = datetime.now() - startTime

print ("\n(Script running time: " + str(time) + ")")
