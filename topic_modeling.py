#coding=utf8
'''
# Anna Bonazzi, 14/09/2017

Topic modeling script to identify document topics with LDA (Latent Dirichlet Allocation). 
Based on model from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

'''
#--------------------------
# VARIABLES FOR USER TO CHANGE
input_file = '/path/to/file.txt'
output_file = 'path/to/saved_topics.txt'
topics_number = 5
words_per_topic = 6
lang = 'english' # Doc language (lower case)
#--------------------------
# Libraries
# To time the script
from datetime import datetime
startTime = datetime.now()

import os, glob, re
# If needed: first run with nltk.download()
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim (only python 2! .decode('utf-8'))
# If python3: install with "pip2 install gensim", then run script with "python2 script.py"
import gensim
from gensim import corpora
#--------------------------
# 1) Use different strings as docs:

doc1 = "Elektrizität (von griechisch ἤλεκτρον ēlektron „Bernstein“) ist der physikalische Oberbegriff für alle Phänomene, die ihre Ursache in ruhender oder bewegter elektrischer Ladung haben."
doc2 = " Dies umfasst viele aus dem Alltag bekannte Phänomene wie Blitze oder die Kraftwirkung des Magnetismus. Der Begriff Elektrizität ist in der Naturwissenschaft nicht streng abgegrenzt, es werden aber bestimmte Eigenschaften zum Kernbereich der Elektrizität gezählt."

# Compile documents
docs = [doc1, doc2]
counter = 0
for i in range (0, len(docs)):
	counter += 1
	docs[i] = docs[i].decode('utf-8')

'''
# 2) Use original file's paragraphs as different docs

#files = glob.glob("/input_folder/B*.htm")
#for fl in files:
#	doc_name = fl[70:-4]

docs = []
with open (input_file, "r") as f:
	my_doc = f.readlines() # Text as list, elements are paragraphs
	for doc in my_doc:
		doc = doc.decode("utf-8")
		docs.append(doc)
'''

# Cleaning and preprocessing
stop = set(stopwords.words(lang)) # Also add custom "useless" words, such as stop = stopwords.words('english') + ['rt', 'via']
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
	stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
	punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
	normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
	return normalized

doc_clean = [clean(doc).split() for doc in docs]

# Preparing Document-Term Matrix

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our corpus, where every unique term is assigned an index. 

dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Running LDA Model

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=topics_number, id2word = dictionary, passes=50)

# Results
results = (ldamodel.print_topics(num_topics=topics_number, num_words=words_per_topic))

fhandle = open (output_file, 'a')
for r in results:
	print ('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + ')).encode('utf-8')))
	fhandle.write('Topic '+str(r[0] + 1)+':\t'+str(', '.join(r[1].split(' + ')).encode('utf-8')) + '\n\n')
fhandle.close()	
# New document starts

#--------------------------
# To time the script
time = datetime.now() - startTime

print ("\n(Script running time: " + str(time) + ")")
