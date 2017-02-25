import os, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import spacy
import math
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load('en')
def load_vocab():    
    all_words = list({w for w in nlp.vocab if w.has_vector and \
        w.orth_.islower()})
    all_words = [w for w in all_words if w.prob > -15]
    unique = set()
    for w in all_words:
        w2 = nlp(w.orth_)[0]
        if not w2.lemma_ in unique:
            if not w2.tag_ == 'NNS':
                unique.add(w)
    all_words = list(unique)
    return all_words
all_words = load_vocab()

# example:
# a is 'man'
# a_star is 'woman'
# b is 'king'
# b_star is to be guessed as 'queen'

def cos3mul(a, a_star, b, b_star):
    a_norm = norm(a)
    b_norm = norm(b)
    b_star_norm = norm(b_star)
    a_star_norm = norm(a_star)
    n1 = dot(b_star, b) / (b_star_norm * b_norm)
    n1 = (n1 + 1) / 2
    n2 = dot(b_star, a_star) / (b_star_norm * a_star_norm)
    n2 = (n2 + 1) / 2
    d1 = dot(b_star, a) / (b_star_norm * a_norm)
    d1 = (d1 + 1) / 2
    return n1 * n2 / d1 

def slow_analogy(a, a_star, b):
    a = nlp.vocab[a]
    a_star = nlp.vocab[a_star]
    b = nlp.vocab[b]
    clust_mean = (a_star.cluster + b.cluster) / 2
    objective = lambda x: cos3mul(a.vector, a_star.vector, b.vector, x.vector)
    ranked = sorted(all_words, key = lambda w: objective(w), reverse = True)
    for word in ranked[:10]:
        if word not in [a, a_star, b]:   
            print(word.orth_)

queries = [w for w in nlp.vocab if w.prob >= -15]
queries = [w for w in queries if w.is_lower]
queries = [w for w in queries if nlp(w.orth_)[0].pos_ == 'NOUN']
def get_similar(word):
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), 
                           reverse=True)
    out = []
    for el in by_similarity[:10]:
        out.append(el.orth_)
    return out

