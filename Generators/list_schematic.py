import os, string, pickle
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Utilities')
import text_fun
os.chdir(BlenderPath + '/Evaluators')
import ksmirnov_fun
import wikipedia
import gensim
import nltk
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

googleList = pickle.load( open('../fulltext.p', 'rb'))
seed_term = pickle.load( open('../search_text.p', 'rb'))
textList = [text_fun.prune(doc) for doc in googleList]
article = wikipedia.page('3D printing').content
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(textList)

header = wikipedia.summary(seed_term)
header = header[0:header.find('\n')]
print(ksEvaluator(header))
print(ksEvaluator(header.replace('sports', 'recreation')))

candidates = []
for item in googleList:
    item = text_fun.prune(item, stem = False, english_dictionary_words = True)
    candidates.extend(item)
candidates = list(set(candidates))
candidates_blob = TextBlob(' '.join(candidates), 
                           pos_tagger = PerceptronTagger())

ok_tags = ['NN']
candidates = []
for item in candidates_blob.tags:
    if item[1] in ok_tags:
        candidates.append(item)
        print(item[0])

header_trim = [w for w in header.split() if w not in 
    stopwords.words('english')]
header_trim = ' '.join(header_trim)
header_blob = TextBlob(header_trim, pos_tagger = PerceptronTagger())
header_tags = list(set(header_blob.tags))
baseline = ksEvaluator(header, verbose = True)


# Brute force-----------
idea_list = []
for item in candidates:
    if item[1] == 'NN':
        for target in header_tags:
            if target[1] == 'NN':
                #new_idea = item[0] + ' ' + target[0]
                #new_idea = item[0] + ' ' + header 
                new_idea = header.replace(target[0], item[0], 1)
                idea_score = ksEvaluator(new_idea)
                if idea_score < baseline:
                    #new_idea_full = header.replace(target[0], item[0])
                    new_idea_full = '%s is related to %s.  What if you replaced the idea of %s in %s with %s?' % (seed_term, target[0], target[0], seed_term, item[0]) 
                    pair = (new_idea_full, idea_score)
                    idea_list.append(pair)
                    print(idea_score)

ideas = list(set(idea_list))
sorted_ideas = sorted(ideas, key = lambda tup: tup[1])
ideas = [i for i in ideas if i[1] == sorted_ideas[0][1]]




# Word2Vec beginnings-----
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = sent_detector.tokenize(article)
exclude = set(string.punctuation)
for i, sentence in enumerate(sentences):
    temp = ''.join(ch for ch in sentence if ch not in exclude)
    sentences[i] = text_fun.prune(temp, stem = False)
mod = gensim.models.Word2Vec(sentences)

# If you're finished training the model
mod.init_sims(replace = True)


idea_list = []
candidates = []
candidate_words = list(mod.vocab)
cblob = TextBlob(' '.join(candidate_words), pos_tagger = PerceptronTagger())
candidate_word_tags = cblob.tags
for i, item in enumerate(candidate_words):
    if candidate_word_tags[i][1] in ok_tags:
        candidates.append(item)

for candidate in candidates:
    if candidate in mod.vocab:
        sims = []
        for target in header_tags:
            if target[1] == 'NN' and target[0] in mod.vocab:
                temp_tuple = (mod.similarity(target[0], candidate), target[0])
                sims.append(temp_tuple)
                if sims:
                    best_tuple = min(sims, key = lambda t: t[0])
                    new_idea = header.replace(best_tuple[1], candidate, 1)
                    idea_score = ksEvaluator(new_idea)
                    if idea_score < baseline:
                        pair = (new_idea, idea_score)
                        idea_list.append(pair)
                        print(idea_score)

ideas = list(set(idea_list))
sorted_ideas = sorted(ideas, key = lambda tup: tup[1])


