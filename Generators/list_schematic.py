import os, string, pickle
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Utilities')
import text_fun
os.chdir(BlenderPath + '/Evaluators')
import ksmirnov_fun
import wikipedia
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

googleList = pickle.load( open("../fulltext.p", "rb"))
textList = [text_fun.prune(doc) for doc in googleList]
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(textList)

header = wikipedia.summary("3D printing")
header = header[0:header.find('\n')]
print(ksEvaluator(header))
print(ksEvaluator(header.replace('additive', 'subtractive')))

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
baseline = ksEvaluator(header)
idea_list = []
for item in candidates:
    if item[1] == 'NN':
        for target in header_tags:
            if target[1] == 'NN':
                #new_idea = header.replace(target[0], item[0])
                #new_idea = item[0] + ' ' + target[0]
                new_idea = item[0] + ' ' + header 
                idea_score = ksEvaluator(new_idea)
                if idea_score < baseline:
                    pair = (new_idea, idea_score)
                    idea_list.append(pair)
                    print(idea_score)

ideas = list(set(idea_list))
sorted_ideas = sorted(ideas, key = lambda tup: tup[1])
ideas = [i for i in ideas if i[1] == sorted_ideas[0][1]]

# Perhaps use the outline of the wikipedia article as a structure


