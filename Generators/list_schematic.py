import os, string, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from generators import schema_fun
from utils import text_fun
from utils.wiki_sim import wiki_query
from evaluators import ksmirnov_fun
import wikipedia
import gensim
import nltk
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger


seed_term = pickle.load( open('search_text.p', 'rb'))
seed_term = seed_term.lower()
article = wikipedia.page(seed_term).content
goog_list = pickle.load( open('fulltext.p', 'rb'))
text_list = [text_fun.prune(doc) for doc in goog_list]
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(text_list)

header = wikipedia.summary(seed_term)
header = header[0:header.find('\n')]

candidates = []
for item in goog_list:
    item = text_fun.prune(item, stem=False, english_dict=True)
    candidates.extend(item)
candidates = list(set(candidates))
candidates_blob = TextBlob(' '.join(candidates), 
                           pos_tagger=PerceptronTagger())

ok_tags = ['NN']
candidates = []
for item in candidates_blob.tags:
    if item[1] in ok_tags:
        candidates.append(item)

header_trim = [w for w in header.split() if w not in 
    stopwords.words('english')]
header_trim = ' '.join(header_trim)
header_blob = TextBlob(header_trim, pos_tagger=PerceptronTagger())
header_tags = list(set(header_blob.tags))
baseline = ksEvaluator(header, verbose=True)

ref_concepts = schema_fun.get_ref_concepts(seed_term, method='slow')

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = text_fun.w2v_sent_prep(article, sent_detector)
ref_arts = []
for ref_concept in ref_concepts:
    try:
        ref_article = wikipedia.page(ref_concept).content
        ref_sentences = text_fun.w2v_sent_prep(ref_article, 
            sent_detector)
        ref_arts.append(ref_sentences) 
        sentences.extend(ref_sentences)
        print('Got article for %s' % ref_concept) 
    except wikipedia.exceptions.DisambiguationError:
        pass

# May want to remove targets for which no article is found, since
# the model won't be great on the analogies there, although, maybe not
targets = [element[0] for element in header_tags if element[1] in ok_tags]
targets = [t for t in targets if t not in set(['==', '===', '(', ')'])]
target_arts = []
for target in targets:
    try:
        if seed_term != target:
            target_article = wikipedia.page(target).content
            print('Got a target article for %s' % target)
            target_sentences = text_fun.w2v_sent_prep(target_article, 
                sent_detector)
            target_arts.append(target_sentences) 
            sentences.extend(target_sentences)
    except wikipedia.exceptions.DisambiguationError:
        pass

flat_sentences = [word for sublist in sentences for word in sublist]
blob_sentences = ' '.join(flat_sentences)
blob = TextBlob(blob_sentences, pos_tagger=PerceptronTagger())
sentences_tags = list(set(blob.tags))
ok_words = [element[0] for element in sentences_tags \
    if element[1] in ok_tags]

model = gensim.models.Word2Vec(sentences, sg=1, negative=10)
targets = [target for target in targets if target in model.vocab]
ref_concepts = [rc.lower() for rc in ref_concepts if rc.lower() in model.vocab]
new_ideas = []
seed_term = seed_term.split()
seed_term = seed_term[len(seed_term) - 1]
for target in targets:
    if target != seed_term:
        print('Target: %s' % target)
        for ref_concept in ref_concepts:
            candidates = model.most_similar(positive=[target, ref_concept], 
                negative=[seed_term])
            candidates = [el[0] for el in candidates]
            for candidate in candidates:
                if candidate in ok_words:
                    score = ksEvaluator(article.replace(target, 
                        candidate))
                    next_idea = \
                    'Try using the %s from a %s to make a new kind of %s.' % \
                        (candidate, ref_concept, seed_term)
                    out = (next_idea, target, ref_concept, score, candidate)
                    new_ideas.append(out)

new_ideas2 = schema_fun.limit_filter(4, new_ideas, max_num=3)
new_ideas2 = schema_fun.limit_filter(2, new_ideas2, max_num=5)

new_ideas2.sort(key=lambda x: x[3])
seen = set()

# sneaks a computation into list comprehension using
# the last condition
new_ideas2 = [item for item in new_ideas2 if item[0] \
    not in seen and not seen.add(item[0])] 

ni = [el[0] for el in new_ideas2]
with open('aux/' + seed_term + '_ideas.txt', 'wb') as f:
    f.write('\n'.join(map(str, ni)).encode('utf8'))




