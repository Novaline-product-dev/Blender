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
article = wikipedia.page(seed_term).content
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

mod = gensim.models.Word2Vec.load_word2vec_format(BlenderPath + 
	'/Aux/deps.words.vector', binary = False)
mod.init_sims(replace = True)

ref_concepts = mod.most_similar(seed_term) # get reference concepts for seed_term
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

new_ideas = []
targets = [element[0] for element in header_tags if element[1] in ok_tags]
for target in targets:
    target_article = wikipedia.page(target).seed_term
    for i in range(0, len(ref_concepts)):
        new_idea_i = header.replace(target, new_word)
  

# mod.most_similar(positive = ['polyurethane', 'surfboard'], negative = ['skateboard'])
#
# That will return a list of good matches.  All of them might work.  
# In this particular example it returns these:
# [('neoprene', 0.8313905596733093), ('dacron', 0.8303178548812866), 
# ('gauze', 0.8275730609893799), ('fiberboard', 0.826744556427002), 
# ('silicone', 0.8266098499298096), ('polystyrene', 0.8250176906585693), 
# ('horsehair', 0.8227001428604126), ('elastomer', 0.8209028244018555), 
# ('polypropylene', 0.8173956871032715), ('epoxy', 0.8171824216842651)]

# Then the quesiton is: can you replace polyurethane with neoprene?  


# Following is to train a word2vec model on a particular wikipedia article

#sentences = sent_detector.tokenize(article)
#exclude = set(string.punctuation)
#for i, sentence in enumerate(sentences):
#    temp = ''.join(ch for ch in sentence if ch not in exclude)
#    sentences[i] = text_fun.prune(temp, stem = False)
#mod = gensim.models.Word2Vec(sentences)
#mod.init_sims(replace = True)


