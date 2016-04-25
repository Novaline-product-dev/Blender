import string
import re
from scipy import stats
import numpy as np
from numpy import *
import pandas as pd
from statsmodels.distributions import empirical_distribution as ed
from gensim import utils
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def hasNumber(stringToCheck):
      """Checks string for numbers, returns a boolean."""
	return bool(re.search(r'\d', stringToCheck))

def rmPunct(dirtyStr):
      """Removes punctuation, returns resulting string"""
	splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
	cleanStr = ''.join(splitCleanStr)
	return(cleanStr)

def cdf(array):
      """This takes a 2D array (matrix) of jaccard indices and returns the cdf values on a grid with 500 points equally spaced from 0 to 1.
      """
	array = np.array(array)
	utVec = np.diagonal(array)
	for i in range(1, array.shape[0]):
		utVec = np.concatenate([utVec, np.diagonal(array, i)])
	xgrid = np.linspace(0, 1, 500)
	ecdf = ed.ECDF(utVec)
	yvals = ecdf(xgrid)
	return(yvals)

def ks(cdfVec1, cdfVec2):
      """ Computes the Kolmogorov-Smirnov Distance between 2 cdf vectors."""
	return(max(abs(cdfVec1 - cdfVec2)))

def prune(doc):
      """This takes a single document and tokenizes the words, removes
      undesirable elements, and prepares it to be loaded into a dictionary.
      """
      # Tokenize the document and make it lowercase
      temp = utils.simple_preprocess(doc.lower())

      # Remove freestanding punctuation and punctuation in words
      temp = [w for w in temp if w not in string.punctuation]
      temp = [rmPunct(w) for w in temp]

      # Remove specific tokens
      temp = [w for w in temp if w not in set(['[', ']', "'", '\n', 'com'])]

      # Remove stopwords
      temp = [w for w in temp if w not in stopwords.words('english')]

      # Stem the remaining words
      stemmer = SnowballStemmer('english')
      temp = [stemmer.stem(w) for w in temp]

      return temp
