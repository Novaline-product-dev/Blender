import pickle, os, string, random
import numpy as np 
import scipy as sp 
import pandas as pd 
import matplotlib.pyplot as plt 
import nltk
import networkx as nx
import textFunctions
from gensim import corpora, models, similarities, utils

# The next line throws a warning, but I checked and the sklearn dev team says don't worry about it.
from sklearn.feature_extraction import text 
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

os.chdir(os.getenv('HOME') + '/Documents/Blender')
textList = pickle.load( open("output.p", "rb"))

stemmer = SnowballStemmer('english')
for i, doc in enumerate(textList):
	temp = utils.simple_preprocess(doc) # tokenize
	
	# remove words with numbers
	temp = [w for w in temp if not textFunctions.hasNumber(w)]

	# remove freestanding punctuation, and punctuation in words
	temp = [w for w in temp if w not in string.punctuation]
	temp = [textFunctions.rmPunct(w) for w in temp]
	
	# remove characters specified by me
	temp = [w for w in temp if w not in set(['[', ']', '\'', 
		'\n', 'com'])]

	# remove stopwords.  nltk is case-sensitive: use lowercase.  This step has to be done last, after removing punctuation, etc.
	temp = [w for w in temp if w not in stopwords.words('english')]

	# stemming is usually done, but in this case we want human readable format. We'll have to explore this issue. 
	# temp = [stemmer.stem(w) for w in temp]

	# reversing the split performed above
	textList[i] = ' '.join(temp)

vectorizer = text.CountVectorizer() # initializes a counter from sklearn

# the counter creates a dtm from textList 
dtm = vectorizer.fit_transform(textList) 

# dtm uses a method to convert itself to an array
dtm = dtm.toarray()
vocab = vectorizer.get_feature_names() # get all the words
ranks = ['Rank %d' %(i + 1) for i in range(dtm.shape[0])] # just labeling

# Turns dtm into a pandas DataFrame (based on the dataframe object in R)
dtm = pd.DataFrame(dtm, index = ranks, columns = vocab) 
tdm = dtm.transpose() # term-doc mat = transpose of doc-term mat

# get the vocab ordered by frequency across all pages
idx = tdm.sum(axis = 1).sort_values(ascending = False).index 
tdm = tdm.ix[idx] # sort the term-doc mat by word frequency
totals = tdm.sum(axis = 1)

# Below is a very heavy-handed way of making the network more manageable.  Just remove infrequent words.
wordFreqThreshold = 30  
tdm = tdm[totals > wordFreqThreshold] # remove rows for infrequent words
totals = totals[totals > wordFreqThreshold]

# Crossproduct of term-doc matrix with itself
ttm = np.dot(tdm, tdm.transpose()) # term-term matrix, or adjacency matrix
ttm = np.matrix(ttm)
np.fill_diagonal(ttm, 0)

new_stimulus_index = int(len(totals) / 2)
print(totals.index[new_stimulus_index])

# Plot the word network
G = nx.from_numpy_matrix(ttm)
labelMap = dict(zip(G.nodes(), list(totals.index)))
G = nx.relabel_nodes(G, labelMap)
pos = nx.spring_layout(G)
nx.draw(G, node_size = 0, pos = pos, alpha = 0.04)  
nx.draw_networkx_labels(G, pos = pos, font_color = '#2ca25f')
plt.show() 













