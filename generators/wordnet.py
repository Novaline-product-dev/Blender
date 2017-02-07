import os, string, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import wikipedia
from utils import text_fun
from nltk.corpus import wordnet as wn
from evaluators import ksmirnov_fun


nlp = text_fun.nlp_prune
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
        if el.hypernyms()[0].lemmas()[0].name() != seed_term:
            el_name = el.lemmas()[0].name()
            if el_name in nlp.vocab:
                if nlp.vocab[el_name].prob > -14:
                    el_meros = el.part_meronyms()
                    if el_meros:
                        name = el.lemmas()[0].name()
                        if name != seed_term:
                            sim = nlp.vocab[el_name].similarity(nlp.vocab[seed_term])
                            tup = (name, el_meros, sim)
                            meronyms.append(tup)
seen = set()
meros = []
for el in meronyms:
    if el[0] not in seen:
        meros.append(el)
        seen.add(el[0])
meros = sorted(meros, key=lambda x:x[2], reverse=True)
for el in meros:
    print(el, '\n')

new_ideas = []
seen1 = set()
seen2 = set()
for el in meros:
    if el[0] not in seen1: 
        new_ideas.append('Blend a %s and a %s' %(seed_term, el[0]))
        seen1.add(el[0])
    if el[2] > 0.3:
        for meronym in el[1]:
            name = meronym.lemmas()[0].name()
            if (el[0] != name) and (name not in seen2):
                if name[0] in ['a', 'e', 'i', 'o', 'u']:
                    idea = 'A %s with an %s' %\
                        (seed_term, name)
                else:
                    idea = 'A %s with a %s' %\
                        (seed_term, name)
                new_ideas.append(idea)
                seen2.add(name)

for i, idea in enumerate(new_ideas):
    tup = (idea, ksEvaluator(idea.split()))
    new_ideas[i] = tup

new_ideas = sorted(new_ideas, key=lambda x:x[1])
for idea in new_ideas:
    print(idea[0])