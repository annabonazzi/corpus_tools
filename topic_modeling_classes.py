#coding=utf8
'''
# Anna Bonazzi, 14/09/2017

Script to model document topics with LDA (Latent Dirichlet Allocation). Sample script assembled from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

The script extracts texts with chosen attributes (language, class) from the corpus

Works only for python2 (gensim currently unavailable for python3).
'''
# VARIABLES FOR USER TO CHANGE

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/topics_folder/'
topic_number = 5
words_per_topic = 6
min_freq = 5 # Minimum acceptable word frequency (rare words are ignored)
lang = 'en'
classes = ['pab_energiedienstleister_hersteller', 'pab_foren', 'pab_mobilitaetsdienstleister', 'pab_ngo', 'pab_verbraucher', 'pbv_bildung', 'pbv_fachzeitung', 'pbv_newsdienste', 'pbv_tageszeitung', 'pbv_wochenzeitung', 'peb_foren', 'peb_wissenschaft', 'pfu_bund', 'pfu_foren', 'pfu_gemeinde', 'pfu_initiativ_referendumskomitees', 'pfu_kanton', 'pfu_kommission', 'pfu_partei', 'pfu_projekt', 'pfu_regionale_behoerden-verbuende', 'pfu_stadt']
#---------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim (only python 2! .decode('utf-8'))
# if python3: install with "pip2 install gensim", then run script with "python2 script.py"
import gensim
from gensim import corpora
#---------------------------
# 1) Prepares text to be modeled as list of strings
counter = 0
for cl in classes:
	flag = 0
	fhandle = open (output_folder+cl+'_'+lang+'_topics.txt', 'a')
	counter += 1
	print ('\n\nFor class ' + cl + ':\n')
	text_counter = 0
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
				chunk.append(line.decode('utf-8'))
			  	# Searches for chosen lang/class combination
				regex = re.search('language="'+lang+'".*?subclass="'+cl+'".*?', ''.join(chunk))
				if regex:
					for word in chunk:
						if '<' not in word and '@card@' not in word and '©'.decode('utf-8') not in word:
							doc.append(word)
					docs.append(' '.join(doc))
				chunk = []
				doc = []
				text_counter += 1
				if '00000' in str(text_counter):
					print (str(text_counter))
	if len(docs) < 1:
		flag = 1 # Skips topic modeling if the class is empty		
		
#-------------------------
	# 2) Starts topic modeling
	if flag == 0:
		print ('Starting topic modeling')
		# Cleaning and preprocessing
		langs = {'fr' : 'french', 'de' : 'german', 'it' : 'italian', 'en' : 'english'}
		stop = set(stopwords.words(langs[lang]) + ['avoir', 'e', 'aucun']) # Also add custom "useless" words, such as stop = stopwords.words('english') + ['rt', 'via']
		exclude = set(string.punctuation)
		lemma = WordNetLemmatizer()
		def clean(doc):
			word_count = {}
			for word in doc.split(' '): # Prepares to skip words with low freq
				if word in word_count:
					word_count[word] += 1
				else:
					word_count[word] = 1
			stop_free = " ".join([word for word in doc.lower().split(' ') if word not in stop and word_count[word] > min_freq])
			punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
			normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
			return normalized
	
		doc_clean = [clean(doc).split() for doc in docs]

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
