import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import wikipedia
from utils import text_fun
#from utils.wiki_sim import wiki_query
from gensim.models import Word2Vec
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from nltk.corpus import stopwords

def get_ref_concepts(seed_term, method='quick'):
    if method == 'quick':
        seed_term = seed_term.split()
        seed_term = seed_term[len(seed_term) - 1]
        mod = Word2Vec.load_word2vec_format('aux/deps.words.vector', 
            binary=False)
        mod.init_sims(replace=True)
        out = mod.most_similar(seed_term) 
        out = [item[0] for item in out]
        return out
    elif method == 'LSI':
        out = wiki_query.similar(seed_term)
        out = [el for el in out if el.lower() != seed_term]
        return out
    else:
        out2 = wiki_query.similar(seed_term)
        out2 = [el for el in out2 if el.lower() != seed_term]
        seed_term = seed_term.split()
        seed_term = seed_term[len(seed_term) - 1]
        mod = Word2Vec.load_word2vec_format('aux/deps.words.vector', 
            binary=False)
        mod.init_sims(replace=True)
        out1 = mod.most_similar(seed_term) 
        out1 = [item[0] for item in out1]
        out1.extend(out2)
        return out1

def limit_filter(tuple_index, new_ideas, max_num=3, score_index=3):
    items = set([el[tuple_index] for el in new_ideas])
    out = []
    for item in items:
        sub_ideas = [el for el in new_ideas if el[tuple_index] == item]
        if sub_ideas:
            if max_num == 1:
                out.extend(min(sub_ideas, key=lambda x: x[score_index]))
            else:
                ranked_sub = sorted(sub_ideas, key=lambda x: x[score_index])
                out.extend(ranked_sub[0:(max_num - 1)])
    return out

def get_candidates(goog_list, ok_tags):
    candidates1 = []
    for item in goog_list:
        item = text_fun.prune(item, stem=False, english_dict=True)
        candidates1.extend(item)
    candidates1 = list(set(candidates1))
    candidates_blob = TextBlob(' '.join(candidates1), 
                               pos_tagger=PerceptronTagger())
    candidates2 = []
    for item in candidates_blob.tags:
        if item[1] in ok_tags:
            candidates2.append(item)
    return candidates2 

def get_header_tags(seed_term):
    header = wikipedia.summary(seed_term)
    header = header[0:header.find('\n')]
    header_trim = [w for w in header.split() if w not in 
        stopwords.words('english')]
    header_trim = ' '.join(header_trim)
    header_blob = TextBlob(header_trim, pos_tagger=PerceptronTagger())
    header_tags = list(set(header_blob.tags))
    return header_tags