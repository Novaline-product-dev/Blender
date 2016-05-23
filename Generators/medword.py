import pickle, os, string, random
import numpy as np 
import pandas as pd
import nltk
from gensim import corpora, models, similarities, utils
os.chdir(os.getenv('HOME') + '/Documents/Blender/Utilities')
import text_fun

def median_words(path_to_inputs, num_ideas = 30):
    textList = pickle.load( open("fulltext.p", "rb"))
    textList = [text_fun.prune(doc) for doc in textList]

    dictionary = corpora.Dictionary(textList) # collects stats for each word
    corpus = [dictionary.doc2bow(doc) for doc in textList] 
    lsi = models.LsiModel(corpus, id2word = dictionary, 
        num_topics = len(textList))

    search_text = pickle.load(open('search_text.p', 'rb')) # Loads the search text
    index = similarities.MatrixSimilarity(lsi[corpus])

    searchWords = []
    for text in textList:
        searchWords.extend(text)
    searchWords = set(searchWords)

    simList = []
    wordList = []
    for word in searchWords:
        wordList.extend([word])
        phrase = search_text + ' ' + word
        vec_repr = dictionary.doc2bow(phrase.split())
        vec_lsi = lsi[vec_repr] # convert the query to LSI space
        sim = sum(index[vec_lsi])
        simList.extend([sim])

    # new stimulus words
    simFrame = pd.DataFrame(simList, index = wordList, 
                            columns = ['Similarity'])
    medDistFrame = abs(simFrame - simFrame.median())
    idxMed = medDistFrame.sort_values(by = 'Similarity', ascending = True).index
    newStimulusWords = pd.Series(idxMed)
    counter = 0
    ideaList = []
    for word in newStimulusWords:
        if counter >= num_ideas:
            break
        wordTag = nltk.pos_tag([word])[0][1]
        if wordTag in ['NN', 'NNP']:
            counter = counter + 1
            ideaList.append('Try blending %s with a %s \n' %(search_text, word))
        elif wordTag in ['NNS', 'NNPS']:
            counter = counter + 1
            ideaList.append('Try blending %s with %s \n' %(search_text, word))
        elif wordTag in ['JJ']:
            ideaList.append('Try making  %s more %s \n' %(search_text, word))
            counter = counter + 1
        elif wordTag in ['JJS', 'RBS']:
            ideaList.append('Imagine the %s version of %s \n' %(word, search_text))
            counter = counter + 1
        elif wordTag in ['JJR', 'RBR']:
            ideaList.append('Imagine a %s version of %s \n' %(word, search_text))
            counter = counter + 1
        elif wordTag in ['RB']:
            ideaList.append('How would %s change if you implemented it %s? \n' %(search_text, word))
            counter = counter + 1
        elif wordTag in ['VB']:
            ideaList.append('How could you %s with %s? \n' %(word, search_text))
            counter = counter + 1

    return ideaList
