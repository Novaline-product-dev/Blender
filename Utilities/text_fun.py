import string
import re
import numpy as np
import enchant
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from gensim import utils
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

class WikiCorpus(object):
    def __init__(self, titles_path, files, gensim_dictionary):
        self.dictionary = gensim_dictionary
        self.titles = []
        if os.path.isfile(titles_path):
            with open(titles_path, 'r') as f:
                for line in f:
                    self.titles.extend(line.strip('\n'))
            print('Corpus titles loaded from titles.txt')
        else: 
            for file_name in files:
                print(file_name)
                self.titles.extend(title_extractor(file_name))

    def __iter__(self):
        for i, file_name in enumerate(files):
            docs = text_extractor(file_name)
            for doc in docs:
                yield self.dictionary.doc2bow(prune(doc))
            print(time(), '%i files added to corpus.' %(i + 1))

    def save_titles(self, path):
        with open(path, 'wb') as f:
            for title in self.titles:
                to_write = ''.join((title, '\n'))
                f.write(to_write.encode('utf8'))
