import os, string
import re
import numpy as np
import enchant
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
from gensim import utils
from lxml import html
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn import feature_extraction 


def rm_punct(in_string):
    """Removes punctuation, returns resulting string"""
    split_string = [ch for ch in in_string if ch not in string.punctuation]
    out_string = ''.join(split_string)
    return(out_string)

def prune(doc, stoplist = None, stem = True, 
          english_dictionary_words = False):
    """This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    """
    temp = utils.simple_preprocess(doc.lower())
    temp = [w for w in temp if w not in string.punctuation]
    temp = [rm_punct(w) for w in temp]
    if stoplist:
        temp = [w for w in temp if w not in stoplist]
    temp = [w for w in temp if w not in set(['[', ']', "'", '\n', 'com'])]
    temp = [w for w in temp if w not in stopwords.words('english')]
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

def text_extractor(file_name):
    """Accesses the text of documents in an html file (returns a list)."""
    raw_text = []
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def title_extractor(file_name):
    """Accesses the title of documents in an html file (returns a list)."""
    titles=[]
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

def text_network_plot(textList, wordFreqThreshold = 10):
    """ Plots a pared-down word-word connection network.  If you increase wordFreqThreshold, it pares down the network.  wordFreqThreshold will depend on the size of textList. 

        textList should be a list of unordered lists of words. 
    """
    for i, text in enumerate(textList):
        textList[i] = ' '.join(text)

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

def save_titles(folders, titles_path):
    if os.path.isfile(titles_path):
        print('Titles already on disk at', titles_path)
    else:
        with open(titles_path, 'wb') as outfile:
            for folder in folders:
                print('Getting titles from', folder)
                folder_files = os.listdir(folder)
                folder_files = [f for f in folder_files \
                    if not f.startswith('.')]
                for fname in folder_files:
                    fname2 = folder + '/' + fname
                    f_titles = text_fun.title_extractor(fname2)
                    with open(fname2) as infile:
                        for title in f_titles:
                            print(title)
                            to_write = ''.join((title, '\n'))
                            outfile.write(to_write.encode('utf8'))

def save_articles(folders, articles_path):
    if os.path.isfile(articles_path):
        print('Articles already on disk at', articles_path)
    else:
        with open(articles_path, 'wb') as outfile:
            for folder in folders:
                folder_files = os.listdir(folder)
                folder_files = [f for f in folder_files \
                    if not f.startswith('.')]
                for fname in folder_files:
                    fname2 = folder + '/' + fname
                    print('Adding', fname2)
                    f_articles = text_fun.text_extractor(fname2)
                    with open(fname2) as infile:
                        for article in f_articles:
                            article_tokens = text_fun.prune(article)
                            tokens_string = ' '.join(article_tokens)
                            to_write = ''.join((tokens_string, '\n'))
                            outfile.write(to_write.encode('utf8'))

def line_streamer(path, N=None):
    i = 0
    with open(path, 'rb') as f:
        for line in f:
            if N:
                i += 1
                if i%10000:
                    pct_complete = round(i / N * 100, 2)
                    print('\r %d%% finished' %pct_complete, 
                        end="", flush=True) 
            yield line.decode('utf8', 'ignore').split() 

class WikiCorpus(object):
    def __init__(self, articles_path, gensim_dictionary, N=None):
        self.dictionary = gensim_dictionary
        self.articles_path = articles_path
        if N:
            self.N = N

    def __iter__(self):
        with open(self.articles_path, 'r') as f:
            i = 0
            for line in f:
                i += 1
                if self.N:
                    if i%10000:
                        pct_complete = round(i / self.N * 100, 2)
                        print('\r %d%% finished' %pct_complete, 
                            end="", flush=True) 
                tokens = line.split()
                yield self.dictionary.doc2bow(tokens)


                