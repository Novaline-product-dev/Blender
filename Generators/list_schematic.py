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
print(ksEvaluator(header.replace('polyurethane', 'neoprene')))

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
ref_concepts = [item[0] for item in ref_concepts]
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = text_fun.w2v_sent_prep(article, sent_detector)
ref_arts = []
for ref_concept in ref_concepts:
    try:
        ref_article = wikipedia.page(ref_concept).content
        ref_sentences = text_fun.w2v_sent_prep(ref_article, sent_detector)
        ref_arts.append(ref_sentences) 
        sentences.extend(ref_sentences)
        print('Got article for %s' % ref_concept) 
    except wikipedia.exceptions.DisambiguationError:
        pass

targets = [element[0] for element in header_tags if element[1] in ok_tags]
target_arts = []
for target in targets:
    try:
        if seed_term != target:
            target_article = wikipedia.page(target).content
            print('Got a target article for %s' % target)
            target_sentences = text_fun.w2v_sent_prep(target_article, sent_detector)
            target_arts.append(target_sentences) 
            sentences.extend(target_sentences)
    except wikipedia.exceptions.DisambiguationError:
        pass

flat_sentences = [word for sublist in sentences for word in sublist]
blob_sentences = ' '.join(flat_sentences)
blob = TextBlob(blob_sentences, pos_tagger = PerceptronTagger())
sentences_tags = list(set(blob.tags))
ok_words = [element[0] for element in sentences_tags \
    if element[1] in ok_tags]

model = gensim.models.Word2Vec(sentences)
targets = [target for target in targets if target in model.vocab]
ref_concepts = [rc for rc in ref_concepts if rc in model.vocab]
new_ideas = []
for target in targets:
	print('Target: %s' % target)
    for ref_concept in ref_concepts:
        candidates = model.most_similar(positive = 
            [target, ref_concept], 
            negative = [seed_term])
        candidates = [el[0] for el in candidates]
        for candidate in candidates:
        	if candidate in ok_words:
                score = ksEvaluator(article.replace(str(target), 
                    candidate))
                next_idea = \
                'Try using the %s from a %s to make a new kind of %s.' % \
                    (candidate, ref_concept, seed_term)
                out = (next_idea, target, ref_concept, score)
                new_ideas.append(out)

new_ideas.sort(key = lambda tuple: tuple[3])
seen = set()
new_ideas = [item for item in new_ideas if item[0] \
    not in seen and not seen.add(item[0])]

ni = [el[0] for el in new_ideas]
with open("new_ideas.txt", 'w') as f:
    f.write('\n'.join(map(str, ni)))
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


