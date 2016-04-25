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

def textNetworkPlot(textList, wordFreqThreshold = 10):
    for i, text in enumerate(textList):
        textList[i] = ' '.join(text)

    # initializes a counter from sklearn
    vectorizer = feature_extraction.text.CountVectorizer() 
    dtm = vectorizer.fit_transform(textList) 
    dtm = dtm.toarray()
    vocab = vectorizer.get_feature_names() # get all the words
    ranks = ['Rank %d' %(i + 1) for i in range(dtm.shape[0])] # just labeling
    dtm = pd.DataFrame(dtm, index = ranks, columns = vocab) 
    tdm = dtm.transpose() # term-doc mat = transpose of doc-term mat

    # get the vocab ordered by frequency across all pages
    idx = tdm.sum(axis = 1).sort_values(ascending = False).index 
    tdm = tdm.ix[idx] # sort the term-doc mat by word frequency
    totals = tdm.sum(axis = 1)

    # Remove infrequent words.
    tdm = tdm[totals > wordFreqThreshold] # remove rows for infrequent words
    totals = totals[totals > wordFreqThreshold]

    # Crossproduct of term-doc matrix with itself
    ttm = np.dot(tdm, tdm.transpose()) # term-term matrix, or adjacency matrix
    ttm = np.matrix(ttm)
    np.fill_diagonal(ttm, 0)

    # Plot the word network
    G = nx.from_numpy_matrix(ttm)
    labelMap = dict(zip(G.nodes(), list(totals.index)))
    G = nx.relabel_nodes(G, labelMap)
    pos = nx.spring_layout(G)
    nx.draw(G, node_size = 0, pos = pos, alpha = 0.04)  
    nx.draw_networkx_labels(G, pos = pos, font_color = '#2ca25f')
    plt.show() 