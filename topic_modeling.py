#coding=utf8
'''
# Anna Bonazzi, 14/09/2017

Script to model topics with LDA (Latent Dirichlet Allocation). Sample script assembled from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

'''
# To time the script
from datetime import datetime
startTime = datetime.now()

import os, glob, re
# If needed: first run with nltk.download()
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim (only python 2! .decode('utf-8'))
# if python3: install with "pip2 install gensim", then run script with "python2 script.py"
import gensim
from gensim import corpora
#--------------------------
# VARIABLES FOR USER TO CHANGE
input_file = '/path/to/file.txt'
output_folder = 'path/to/saved_topics/'
topic_number = 5
words_per_topic = 6

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

files = glob.glob("S:\\pools\\l\\L-Korpusgruppe\\Working_Files\\Workshop_CQPWeb\\elektr_korpus\\B*.htm")
counter = 0
for fl in files:
	counter = int(counter) + 1
	doc_name = fl[70:-4]
	docs = []
	with open (fl, "r") as f:
		my_doc = f.readlines() # Text as list, elements are paragraphs
		for doc in my_doc:
			doc = doc.decode("utf-8")
			docs.append(doc)
'''

# Cleaning and preprocessing
langs = 
stop = set(stopwords.words('german')) # Also add custom "useless" words, such as stop = stopwords.words('english') + ['rt', 'via']
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
	stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
	punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
	normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
	return normalized
# 1) If docs is a list
doc_clean = [clean(doc).split() for doc in docs]

# 2) If docs is a string
#doc_clean = [clean(docs).split()]

# Preparing Document-Term Matrix

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 

dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Running LDA Model

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)

# Results
results = (ldamodel.print_topics(num_topics=3, num_words=3))

for r in results:
	print (r)
	# New document starts

#--------------------------
# To time the script
time = datetime.now() - startTime

print ("\n(Script running time: " + str(time) + ")")
