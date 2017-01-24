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
refs = []
seed_term = seed_term.split()[len(seed_term.split()) - 1]
hyper = lambda s: s.hypernyms()
hypo = lambda s: s.hyponyms()
meronyms = []
seed_synset = wn.synsets(seed_term)[0]
seed_hypers = list(seed_synset.closure(hyper, depth=4))
for seed_hyper in seed_hypers:
    for el in list(seed_hyper.closure(hypo, depth=4)):
        el_meros = el.part_meronyms()
        if el_meros:
            name = el.lemmas()[0].name()
            tup = (name, el_meros)
            meronyms.append(tup)
seen = set()
meros = []
for el in meronyms:
    if el[0] not in seen:
        meros.append(el)
        seen.add(el[0])

for el in meros:
    print(el, '\n')

new_ideas = []
for el in meros:
    new_ideas.append('Blend a %s and a %s' %(seed_term, el[0]))
    for meronym in el[1]:
        name = meronym.lemmas()[0].name()
        idea = 'Use the %s from a %s to make a new %s' %\
            (name, el[0], seed_term)
        new_ideas.append(idea)

for idea in new_ideas:
    print(idea, '\n')


#new_ideas2 = []
#defn = seed_synset.definition()
#defn_tags = TextBlob(defn, pos_tagger = PerceptronTagger()).tags
#defn_tags = [el[0] for el in defn_tags if el[1] in set(['NN', 'NNS'])]
#for target in defn_tags:
#    target_synset = []
#    target_synset = wn.synsets(target)
#    if target_synset:
#        target_syn = target_synset[0]
#        target_sisters = target_syn.hypernyms()[0].hyponyms()
#        for sister in target_sisters:
#            sister_name = sister.lemmas()[0].name()
#            new_ideas2.append(defn.replace(target, sister_name))