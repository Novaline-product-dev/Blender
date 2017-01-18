import os, string, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import wikipedia
from utils import text_fun
from nltk.corpus import wordnet as wn
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from evaluators import ksmirnov_fun


seed_term = pickle.load( open('search_text.p', 'rb'))
seed_term = seed_term.lower()
goog_list = pickle.load(open('fulltext.p', 'rb'))
text_list = [text_fun.prune(doc) for doc in goog_list]
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(text_list)
article = wikipedia.page(seed_term).content
def get_names(synlist):
    out = []
    for el in synlist:
        long_name = el.name()
        to_add = long_name[:long_name.find('.')]
        out.append(to_add)
    return out

refs = []
seed_term = seed_term.split()[len(seed_term.split()) - 1]
synset = wn.synsets(seed_term)[0]
hyper3nyms = synset.hypernyms()[0].hypernyms()[0].hypernyms()[0]
for el in hyper3nyms.hyponyms():
    hypernyms = el.hyponyms()
    for item in hypernyms:
        refs.extend(get_names(hypernyms))
print('line 32')
article = article.replace('\n', ' ')
article = article.replace('=', '')
aug = article.split()
candidates = []
for text in text_list:
    candidates.extend(text)
candidates = list(set(candidates))
new_ideas = []
for candidate in candidates:
    temp = list(aug)
    temp.append(candidate)
    score = ksEvaluator(temp)
    print(score)
    tup = (candidate, score)
    new_ideas.append(tup)

new_ideas = sorted(new_ideas, key=lambda x:x[1])    
for new_idea in new_ideas:
    print('Blend a %s and a %s.  Score: %d' \
          %(seed, new_ideas[0], new_ideas[1]))
#def get_defns(seed):
#    seed = wn.synsets(seed, pos=wn.NOUN)[0]
#    defns = []
#    defns.append(seed.definition())
#    hypos = seed.hyponyms()
#    if hypos:
#        for nym in hypos:
#            defns.append(nym.definition())
#    blob = TextBlob(' '.join(defns),
#                    pos_tagger = PerceptronTagger())
#    blob = list(set(blob.tags))
#    blob = [tag[0] for tag in blob if tag[1] == 'NN']
#    blob = [w for w in blob if w not in set([')', '('])]
#    return blob, defns
#
#def sister_terms(synset):
#    out = []
#    for hypernym in synset.hypernyms():
#        hyponyms = hypernym.hyponyms()
#        for hyponym in hyponyms:
#            name = hyponym.name()
#            out.append(name[:name.find('.')])
#    return out
#
#def defn_expand(defn, blob):
#    ideas = []
#    for item in blob:
#        if defn.find(item) != -1:
#            wn_item = wn.synsets(item)[0]
#            sisters = sister_terms(wn_item)
#            for sister in sisters:
#                if sister != item:
#                    to_add = defn.replace(item, 
#                        sister)
#                    ideas.append(to_add)
#    return ideas
#
#blob, defns = get_defns('notebook')
#new_ideas = []
#for defn in defns:
#    new_ideas.extend(defn_expand(defn, blob))#