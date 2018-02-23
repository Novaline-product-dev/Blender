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
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(text_list)

def stim_words(num_ideas = 40):
    searchWords = []
    for text in text_list:
        searchWords.extend(text)
    searchWords = set(searchWords)

    words = []
    if seed_term in nlp.vocab:
        seed_lexeme = nlp.vocab[seed_term]
    else:
        split_term = seed_term.split()
        seed_lexeme = nlp.vocab[split_term[len(split_term) - 1]]
    for word in searchWords:
        if word in nlp.vocab:
            lexeme = nlp.vocab[word]
            if lexeme.prob > -14:
                sim = lexeme.similarity(seed_lexeme)
                if sim < 0.7:
                    tup = (word, sim)
                    words.append(tup)

    #words = sorted(words, key=lambda x:x[1], reverse=True)
    stim_words = [w[0] for w in words]
    for i, stim_word in enumerate(stim_words):
        score = ksEvaluator([seed_term, stim_word])
        stim_words[i] = (stim_word, score)
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