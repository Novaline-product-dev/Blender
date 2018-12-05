import os, string, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from generators import schema_fun
from utils import text_fun
from evaluators import ksmirnov_fun
import wikipedia


with open('search_text.p', 'rb') as f:
	seed_term = pickle.load(f)
seed_term = seed_term.lower()
article = wikipedia.page(seed_term).content
with open('fulltext.p', 'rb') as f:
	goog_list = pickle.load(f)
text_list = [text_fun.prune(doc) for doc in goog_list]
ksEvaluator = ksmirnov_fun.ksFunctionGenerator(text_list)
ks2 = ksmirnov_fun.ksFunctionGenerator(text_list)

ok_tags = ['NN', 'JJ']
header_tags = schema_fun.get_header_tags(seed_term)
targets = [str(el[0]) for el in header_tags if el[1] in ok_tags]
exclude = set(['==', '===', '(', ')', 'etc', 'e.g.'])
targets = [t for t in targets if t not in exclude]
targets = list(set(targets))

ref_concepts = schema_fun.get_ref_concepts(seed_term, method='quick')
model = schema_fun.build_model(seed_term, ref_concepts, targets, article)

# Remove stuff not in the vocab
targets = [target for target in targets if target in model.wv.vocab]
ref_concepts = [rc.lower() for rc in ref_concepts if rc.lower() in model.wv.vocab]

new_ideas = schema_fun.schema_framer(seed_term, targets, 
    ref_concepts, model, ksEvaluator, ok_tags, article)
# location 4 (first argument) is target, 2 is ref_concept
new_ideas2 = schema_fun.limit_filter(4, new_ideas, max_num=3)
new_ideas3 = schema_fun.limit_filter(2, new_ideas2, max_num=5)

new_ideas3.sort(key=lambda x: x[3])
seen = set()
# sneaks a computation into list comprehension using
# the last condition
new_ideas3 = [item for item in new_ideas3 if item[0] \
    not in seen and not seen.add(item[0])] 

ni = [el[0] for el in new_ideas3]
with open('aux/' + seed_term + '_ideas.txt', 'wb') as f:
    f.write('\n'.join(map(str, ni)).encode('utf8'))

