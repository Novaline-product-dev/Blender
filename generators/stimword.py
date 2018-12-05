import pickle, os, string, random
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import spacy 
from utils import text_fun
from evaluators import ksmirnov_fun
import numpy as np 
import pandas as pd
from gensim import corpora, models, similarities, utils


goog_list = pickle.load( open("fulltext.p", "rb"))
text_list = [text_fun.prune(doc) for doc in goog_list]
seed_term = pickle.load(open('search_text.p', 'rb'))
nlp = text_fun.nlp_prune # parser is not used on this one

def stim_words(num_ideas = 40):
    searchWords = []
    for text in text_list:
        searchWords.extend(text)
    searchWords = set(searchWords)

    dictionary = corpora.Dictionary(text_list) 
    corpus = [dictionary.doc2bow(doc) for doc in text_list] 
    lsi = models.LsiModel(corpus, id2word = dictionary, 
        num_topics = len(text_list))
    index = similarities.MatrixSimilarity(lsi[corpus])


    #words = sorted(words, key=lambda x:x[1], reverse=True)
    stim_words = list()
    for word in searchWords:
        phrase = seed_term + ' ' + word
        vec_repr = dictionary.doc2bow(phrase.split())
        vec_lsi = lsi[vec_repr] # convert the query to LSI space
        sim = sum(index[vec_lsi])
        stim_words.append((word, sim))
    
    sim_frame = pd.DataFrame(stim_words)
    sim_frame.index = sim_frame[0]
    sim_frame = sim_frame.drop([0], axis=1)
    sim_frame['med_dist'] = abs(sim_frame - sim_frame.median())
    stim_words = list(zip(sim_frame.index, sim_frame['med_dist']))
    stim_words = sorted(stim_words, key= lambda x:x[1])
    [print(w[1]) for w in stim_words]
    stim_words = [w[0] for w in stim_words]

    
    counter = 0
    ideas = []
    for word in stim_words:
        if counter >= num_ideas:
            break
        tag = nlp(word)[0].tag_
        if tag in ['NN']:
            counter = counter + 1
            ideas.append('Blend a %s with a %s \n' %(seed_term, word))
        elif tag in ['NNS']:
            counter = counter + 1
            ideas.append('Blend %s with %s \n' %(seed_term, word))
        elif tag in ['JJ']:
            ideas.append('Make a %s that is less %s \n' %(seed_term, word))
            counter = counter + 1
        elif tag in ['JJS', 'RBS']:
            ideas.append('A %s version of a %s \n' %(word, seed_term))
            counter = counter + 1
        elif tag in ['JJR', 'RBR']:
            ideas.append('A %s version of a %s \n' %(word, seed_term))
            counter = counter + 1
        elif tag in ['RB']:
            ideas.append('How would %s change if you implemented it %s? \n' %(seed_term, word))
            counter = counter + 1
        elif tag in ['VB']:
            ideas.append('A %s used to %s. \n' %(seed_term, word))
            counter = counter + 1
    return ideas

print(' '.join(stim_words()))