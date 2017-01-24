import os, string
import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
import spacy
from gensim import utils
from lxml import html
from sklearn import feature_extraction 


nlp = spacy.load('en')

def rm_punct(in_string):
    """Removes punctuation, returns resulting string"""
    split_string = [ch for ch in in_string if ch not in string.punctuation]
    out_string = ''.join(split_string)
    return(out_string)

def prune(doc, stoplist=None, lemmatize=True, 
          english_dict=False):
    """This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    """
    custom_rm_list = set(['[', ']', "'", '\n', 'com', '\n\n'])
    temp = nlp(doc)
    temp = [w for w in temp if w.pos_ != 'PUNCT']
    if stoplist:
        temp = [w for w in temp if w.text not in stoplist]
    temp = [w for w in temp if w.text not in custom_rm_list]
    temp = [w for w in temp if not w.is_stop]
    if english_dict:
        temp = [w for w in temp if w in nlp.vocab]
    if lemmatize:
        out = [w.lemma_ for w in temp]
    else:
        out = temp
    return out

def w2v_sent_prep(article, sent_detector):
    sentences = sent_detector.tokenize(article)
    exclude = set(string.punctuation)
    for i, sentence in enumerate(sentences):
        temp = ''.join(ch for ch in sentence if ch not in exclude)
        sentences[i] = prune(temp, lemmatize=False)
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
    idx = tdm.sum(axis = 1).sort_values(ascending = False).index 
    tdm = tdm.ix[idx] # sort the term-doc mat by word frequency
    totals = tdm.sum(axis = 1)
    tdm = tdm[totals > wordFreqThreshold] 
    totals = totals[totals > wordFreqThreshold]
    ttm = np.dot(tdm, tdm.transpose()) 
    ttm = np.matrix(ttm)
    np.fill_diagonal(ttm, 0)
    G = nx.from_numpy_matrix(ttm)
    labelMap = dict(zip(G.nodes(), list(totals.index)))
    G = nx.relabel_nodes(G, labelMap)
    pos = nx.spring_layout(G)
    nx.draw(G, node_size=0, pos=pos, alpha=0.04)  
    nx.draw_networkx_labels(G, pos=pos, font_color='#2ca25f')
    plt.show() 

def prep_save(input_path, titles_path, articles_path, token_min=5):
    if os.path.isfile(titles_path) and os.path.isfile(articles_path):
        print('Prepped files already on disk at', titles_path,
            ' and ', articles_path)
    else:
        articles = text_extractor(input_path)
        titles = title_extractor(input_path)
        titles_out = []
        articles_out = []
        for title, article in zip(titles, articles):
            prepped_title = ''.join((title, '\n'))
            article_tokens = prune(article)
            if len(article_tokens) >= token_min:
                tokens_string = ' '.join(article_tokens)
                prepped_art = ''.join((tokens_string, '\n'))
                titles_out.append(prepped_title)
                articles_out.append(prepped_art)
        assert len(articles_out) == len(titles_out)
        with open(titles_path, 'wb') as f:
            for title in titles_out:
                f.write(title.encode('utf8'))
        with open(articles_path, 'wb') as f:
            for article in articles_out:
                f.write(article.encode('utf8'))

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
