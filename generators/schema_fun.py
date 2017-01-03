import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils.wiki_sim import wiki_query
from gensim.models import Word2Vec

def get_ref_concepts(seed_term, method='quick'):
    if method == 'quick':
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
        mod = Word2Vec.load_word2vec_format('aux/deps.words.vector', 
            binary=False)
        mod.init_sims(replace=True)
        out1 = mod.most_similar(seed_term) 
        out1 = [item[0] for item in out1]
        out2 = wiki_query.similar(seed_term)
        out = [el for el in out if el.lower() != seed_term]
        out1.extend(out2)
        return out1

def limit_filter(tuple_index, new_ideas, max_num=3, score_index=3):
    items = set([el[tuple_index] for el in new_ideas])
    out = []
    for item in items:
        sub_ideas = [el for el in new_ideas if el[tuple_index] == item]
        if sub_ideas:
            if max_num == 1:
                out.append(min(sub_ideas, key=lambda x: x[score_index]))
            else:
                ranked_sub = sorted(sub_ideas, key=lambda x: x[score_index])
                out.append(ranked_sub[0:(max_num - 1)])
    return out