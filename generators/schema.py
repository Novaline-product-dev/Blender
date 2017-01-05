import os, string, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from generators import schema_fun
from utils import text_fun
from evaluators import ksmirnov_fun
import wikipedia
import gensim
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger


seed_term = pickle.load( open('search_text.p', 'rb'))
seed_term = seed_term.lower()
header_tags = schema_fun.get_header_tags(seed_term)
article = wikipedia.page(seed_term).content
goog_list = pickle.load( open('fulltext.p', 'rb'))
text_list = [text_fun.prune(doc) for doc in goog_list]
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(text_list)
ok_tags = ['NN']
targets = [el[0] for el in header_tags if el[1] in ok_tags]
candidates = schema_fun.get_candidates(goog_list, ok_tags) #list of tuples
ref_concepts = schema_fun.get_ref_concepts(seed_term, method='quick')
targets, model, ok_words = schema_fun.build_model(seed_term, 
    ref_concepts, targets, article, ok_tags)
print(model)
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




