import os, string
import spacy
from gensim import utils
from lxml import html


nlp = spacy.load('en')

def prune(doc, stoplist=None, lemmatize=True, english_dict=False):
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
    """Gets body text from html docs produced by wikiextractor."""
    raw_text = []
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def title_extractor(file_name):
    """Gets titles from html docs produced by wikiextractor."""
    titles=[]
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

def line_streamer(path, N=None):
    """Generator function for building the dictionary."""
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
