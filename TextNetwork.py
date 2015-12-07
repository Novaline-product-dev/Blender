import pickle, os, string, random, statistics
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
AuxPath = os.getenv('HOME') + '/Documents/Blender/Aux'
os.chdir(BlenderPath)

import numpy as np 
import scipy as sp 
import pandas as pd 
import matplotlib.pyplot as plt 
import nltk
import networkx as nx
import textFunctions
import enchant 
from gensim import corpora, models, similarities, utils

# The next line throws a warning, but I checked and the sklearn dev team 
# says don't worry about it.
from sklearn import feature_extraction 
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

textList = pickle.load( open("output.p", "rb"))

stemmer = SnowballStemmer('english')
for i, doc in enumerate(textList):
	temp = utils.simple_preprocess(doc) # tokenize
	
	# remove words with numbers
	temp = [w for w in temp if not textFunctions.hasNumber(w)]

	# remove freestanding punctuation, and punctuation in words
	temp = [w for w in temp if w not in string.punctuation]
	temp = [textFunctions.rmPunct(w) for w in temp]
	
	# remove tokens specified by me
	temp = [w for w in temp if w not in set(['[', ']', '\'', 
		'\n', 'com'])]

	# remove stopwords.  nltk is case-sensitive: use lowercase. 
	# This step has to be done last, after removing punctuation, etc.
	temp = [w for w in temp if w not in stopwords.words('english')]

	# stemming is usually done, but in this case we want human readable format. 
	# We'll have to explore this issue. 
	# temp = [stemmer.stem(w) for w in temp]

	# reversing the split performed above
	textList[i] = temp

dictionary = corpora.Dictionary(textList) # collects stats for each word
dictionary.save(AuxPath + '/currentDictionary.dict') # save for later

# This is gensim's style of corpus
corpus = [dictionary.doc2bow(doc) for doc in textList] 
# store to disk, for later
corpora.MmCorpus.serialize(AuxPath + '/textList.mm', corpus) 
lsi = models.LsiModel(corpus, num_topics = len(textList))

search_text = pickle.load(open('output2.p', 'rb'))
index = similarities.MatrixSimilarity(lsi[corpus])

searchWords = []
for text in textList:
	searchWords.extend(text)
searchWords = set(searchWords)

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
for word in newStimulusWords:
	if counter >= 10:
		break
	wordTag = nltk.pos_tag([word])[0][1]
	if wordTag in ['NN', 'NNP']:
		print('Try blending your idea with a %s' %word)
		counter = counter + 1
	elif wordTag in ['NNS', 'NNPS']:
		print('Try blending your idea with %s' %word)
		counter = counter + 1
	elif wordTag in ['JJ']:
		print('Try making your idea more %s' %word)
		counter = counter + 1
	elif wordTag in ['JJS', 'RBS']:
		print('Imagine the %s version of your idea' %word)
		counter = counter + 1
	elif wordTag in ['JJR', 'RBR']:
		print('Imagine a %s version of your idea' %word)
		counter = counter + 1
	elif wordTag in ['RB']:
		print('How would your idea change if you implemented it %s' %word)
		counter = counter + 1
	elif wordTag in ['VB']:
		print('How could you %s with your idea?' %word)
		counter = counter + 1


#print(newStimulusWords)

# An example: the first stimulus word for the concept '3D printing' is 'photo', which suggests that a new possible use for 3D printers is printing photographs with texture or depth.  The fourth stimulus word is 'changeable', which could mean changing the printing material partway through a process, in order to print composite structures.  (When I asked someone else, she said it brougth to mind a less rigid object, so the printer would create a squishy object instead of a totally hard one.  This demonstrates the fact that 2 different humans interacting with this system would generate different ideas, which is another interesting topic for exploration.)  

# These examples are encouraging, but since the other words are mostly useless, we still have some work to do.  Next I plan to use POS tags to help generate more sensible stimuli, by placing the words in a template sentance.  For instance, if the word is a singular noun, the template sentence may be: "try incorporating elements from a ____."  If it is an adjective, the sentence may be: "try making your idea more (or less) ____"




# Below is just for plotting.  Comment out if you don't want the plot
#-------------------------------------------------------------------------------
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
