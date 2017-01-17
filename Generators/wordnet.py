from nltk.corpus import wordnet as wn
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

def get_defns(seed):
    seed = wn.synsets(seed, pos=wn.NOUN)[0]
    defns = []
    defns.append(seed.definition())
    hypos = seed.hyponyms()
    if hypos:
        for nym in hypos:
            defns.append(nym.definition())
    blob = TextBlob(' '.join(defns),
                    pos_tagger = PerceptronTagger())
    blob = list(set(blob.tags))
    blob = [tag[0] for tag in blob if tag[1] == 'NN']
    blob = [w for w in blob if w not in set([')', '('])]
    return blob, defns

def sister_terms(synset):
    out = []
    for hypernym in synset.hypernyms():
        hyponyms = hypernym.hyponyms()
        for hyponym in hyponyms:
            name = hyponym.name()
            out.append(name[:name.find('.')])
    return out

def defn_expand(defn, blob):
    ideas = []
    for item in blob:
        if defn.find(item) != -1:
            wn_item = wn.synsets(item)[0]
            sisters = sister_terms(wn_item)
            for sister in sisters:
                if sister != item:
                    to_add = defn.replace(item, 
                        sister)
                    ideas.append(to_add)
    return ideas

blob, defns = get_defns('notebook')
new_ideas = []
for defn in defns:
    new_ideas.extend(defn_expand(defn, blob))