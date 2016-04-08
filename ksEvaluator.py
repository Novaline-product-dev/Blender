import pickle, os, string, random, statistics
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
AuxPath = os.getenv('HOME') + '/Documents/Blender/Aux'
os.chdir(BlenderPath)

import math
import numpy as np 
from numpy import matlib 
import scipy as sp
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import random
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
textList = [textFunctions.prune(doc) for doc in textList]

for i, text in enumerate(textList):
	textList[i] = ' '.join(text)

# initializes a counter from sklearn
vectorizer = feature_extraction.text.CountVectorizer() 

# the counter creates a dtm from textList 
dtm = vectorizer.fit_transform(textList) 

# dtm uses a method to convert itself to an array
dtm = dtm.toarray()
vocab = vectorizer.get_feature_names() # get all the words

# Turns dtm into a pandas DataFrame (based on the dataframe object in R)
dtm = pd.DataFrame(dtm, columns = vocab) 
tdm = dtm.transpose() # term-doc mat = transpose of doc-term mat

# get the vocab ordered by frequency across all pages
idx = tdm.sum(axis = 1).sort_values(ascending = False).index 
tdm = tdm.ix[idx] # sort the term-doc mat by word frequency
totals = tdm.sum(axis = 1)

# Below is a heavy-handed way of making the corpus more manageable:
# just remove infrequent words
wordFreqThreshold = 10
tdm = tdm[totals > wordFreqThreshold] # remove rows for infrequent words
totals = totals[totals > wordFreqThreshold]

tdmInd = tdm > 0
tdmInd = tdmInd.astype(int)

# Each element is the size of the intersection of the row and column words
interMat = pd.DataFrame.dot(tdmInd, tdmInd.transpose())

# Union(A, B) = A + B - Intersection(A, B)
totalsMat = matlib.repmat(np.diagonal(interMat), interMat.shape[0], 1)
unionMat = totalsMat + np.transpose(totalsMat) - interMat
vocab = list(interMat.index)

# Need to remove words in the original lists
for i, doc in enumerate(textList):
	temp = utils.simple_preprocess(doc)
	temp = list(set(temp) & set(vocab))
	temp.sort()
	textList[i] = temp

# removes empty documents
textList = [doc for doc in textList if doc]

nums = [i for i in range(0, len(vocab))]
wordToNum = dict(zip(vocab, nums))
numToWord = dict(zip(nums, vocab))
jaccardMat = pd.DataFrame(interMat / unionMat, index = vocab, 
	columns = vocab)

# Need to define this function here since it uses some vars in the script.
# bad programming, I know
def jaccard(text):
	index = [wordToNum[word] for word in text]
	out = jaccardMat.iloc[index, index]
	return(out)

cdfMat = np.zeros([500, len(textList)])
for i, doc in enumerate(textList):
		cdfMat[:, i] = tf.cdf(jaccard(doc))

# empirical cdfs averaged across documents in textList yeilds baseline cdf
baseline = cdfMat.sum(1) / len(textList)

searchText = pickle.load( open("output2.p", "rb"))

searchWords = []
for text in textList:
	searchWords.extend(text)
searchWords = list(set(searchWords))


#userIdea = input("What is your idea related to %s?" % searchText)
nWords = len(searchWords)
userIdea = '%s %s' % (searchWords[random.randint(0, nWords)], 
	searchWords[random.randint(0, nWords)])

temp = list(set(set(utils.simple_preprocess(userIdea)) & set(searchWords)))

if len(temp) == 0:
	print('length zero')
else :
	ksVec = np.zeros(len(searchWords)) + 1
	for l, word in enumerate(searchWords):
		temp2 = list(temp)
		temp2.extend([word])
		ksVec[l] = tf.ks(tf.cdf(jaccard(temp2)), baseline)
	print('New word: %s' % searchWords[ksVec.argmin()])





