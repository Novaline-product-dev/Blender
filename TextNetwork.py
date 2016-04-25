import pickle, os, string, random, statistics
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
AuxPath = os.getenv('HOME') + '/Documents/Blender/Aux'
os.chdir(BlenderPath)

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import networkx as nx
import textFunctions
import enchant
from gensim import corpora, models, similarities, utils
from sklearn import feature_extraction 


textList = pickle.load( open("fulltext.p", "rb"))
textList = [textFunctions.prune(doc) for doc in textList]

dictionary = corpora.Dictionary(textList) # collects stats for each word
dictionary.save(AuxPath + '/currentDictionary.dict') # save for later

# This is gensim's style of corpus
corpus = [dictionary.doc2bow(doc) for doc in textList] 
# store to disk, for later
corpora.MmCorpus.serialize(AuxPath + '/textList.mm', corpus) 
lsi = models.LsiModel(corpus, id2word = dictionary, 
	num_topics = len(textList))

search_text = pickle.load(open('search_text.p', 'rb')) # Loads the search text
index = similarities.MatrixSimilarity(lsi[corpus])

searchWords = []
for text in textList:
	searchWords.extend(text)
searchWords = set(searchWords)

# Weed out non-english words
d = enchant.Dict("en_US")
simList = []
wordList = []
for word in searchWords:
	if d.check(word):
		wordList.extend([word])
		phrase = search_text + ' ' + word
		vec_repr = dictionary.doc2bow(phrase.split())
		vec_lsi = lsi[vec_repr] # convert the query to LSI space
		sim = sum(index[vec_lsi])
		simList.extend([sim])


# new stimulus words
simFrame = pd.DataFrame(simList, index = wordList, columns = ['Similarity'])
medDistFrame = abs(simFrame - simFrame.median())
idxMed = medDistFrame.sort_values(by = 'Similarity', ascending = True).index
newStimulusWords = pd.Series(idxMed)
counter = 0
num_items = 30
for word in newStimulusWords:
	if counter >= num_items:
		break
	wordTag = nltk.pos_tag([word])[0][1]
	if wordTag in ['NN', 'NNP']:
		counter = counter + 1
		print('Try blending %s with a %s' %(search_text, word))
	elif wordTag in ['NNS', 'NNPS']:
		counter = counter + 1
		print('Try blending %s with %s' %(search_text, word))
	elif wordTag in ['JJ']:
		print('Try making  %s more %s' %(search_text, word))
		counter = counter + 1
	elif wordTag in ['JJS', 'RBS']:
		print('Imagine the %s version of %s' %(word, search_text))
		counter = counter + 1
	elif wordTag in ['JJR', 'RBR']:
		print('Imagine a %s version of %s' %(word, search_text))
		counter = counter + 1
	elif wordTag in ['RB']:
		print('How would %s change if you implemented it %s?' %(search_text, word))
		counter = counter + 1
	elif wordTag in ['VB']:
		print('How could you %s with %s?' %(word, search_text))
		counter = counter + 1


#print(newStimulusWords)


# Below is just for plotting.  Comment if you don't want the plot
#--------------------------------------------------------------------
for i, text in enumerate(textList):
	textList[i] = ' '.join(text)

# initializes a counter from sklearn
vectorizer = feature_extraction.text.CountVectorizer() 

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

# Below is a very heavy-handed way of making the network more manageable.  
# Just remove infrequent words.
wordFreqThreshold = 10
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
