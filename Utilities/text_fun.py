import string
import re
from scipy import stats
import numpy as np
import enchant
from numpy import *
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from gensim import utils
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn import feature_extraction 

def hasNumber(stringToCheck):
    """Checks string for numbers, returns a boolean."""
    return bool(re.search(r'\d', stringToCheck))

def rmPunct(dirtyStr):
    """Removes punctuation, returns resulting string"""
    splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
    cleanStr = ''.join(splitCleanStr)
    return(cleanStr)

def prune(doc, stoplist = None, stem = True, english_dictionary_words = False):
    """This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    """
    # Tokenize the document and make it lowercase
    temp = utils.simple_preprocess(doc.lower())

    # Remove freestanding punctuation and punctuation in words
    temp = [w for w in temp if w not in string.punctuation]
    temp = [rmPunct(w) for w in temp]

    # Remove words in passed stoplist
    if stoplist:
        temp = [w for w in temp if w not in stoplist]

    # Remove specific tokens
    temp = [w for w in temp if w not in set(['[', ']', "'", '\n', 'com'])]

    # Remove stopwords
    temp = [w for w in temp if w not in stopwords.words('english')]

    # Stem the remaining words
    if stem:
        stemmer = SnowballStemmer('english')
        temp = [stemmer.stem(w) for w in temp]

    if english_dictionary_words:
        d = enchant.Dict("en_US")
        temp = [w for w in temp if d.check(w)]
    return temp

def w2v_sent_prep(article, sent_detector):
    sentences = sent_detector.tokenize(article)
    exclude = set(string.punctuation)
    for i, sentence in enumerate(sentences):
        temp = ''.join(ch for ch in sentence if ch not in exclude)
        sentences[i] = prune(temp, stem = False)
    return sentences

def textNetworkPlot(textList, wordFreqThreshold = 10):
    """ Plots a pared-down word-word connection network.  If you increase wordFreqThreshold, it pares down the network.  wordFreqThreshold will depend on the size of textList. 

        textList should be a list of unordered lists of words. 
    """
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