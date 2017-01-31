import wikipedia
import random
from spacy.en import English
from spacy.symbols import amod


nlp = English()
seed = 'skateboard'
page = wikipedia.page(seed)
seed_word = nlp(seed)[0]
doc = page.content
doc_split = doc.split('\n\n\n=')
doc = doc_split[0]
for sec in doc_split[1:]:
    sec_header = sec[:sec.find('\n') + 1]
    if sec_header.find('History') == -1:
        sec_header = sec_header.replace('=', '')
        sec_header = sec_header.strip()
        clean = sec[sec.find('\n') + 1:].strip()
        print(sec_header)
        doc = doc + ' ' + sec_header + ' ' + clean
doc = doc.replace('=', ' ')
doc = doc.replace('References', '')
doc = doc.replace('\n', ' ')
doc = ' '.join(doc.split())
doc = nlp(doc)

def get_adj_phrases(doc, word):
    out = []
    for el in doc:
        if el.dep_ == 'amod':
            if el.similarity(word) > 0.2:
                out.append(str(el) + ' ' + str(el.head))
    return out


links = [l for l in page.links if seed_word.similarity(nlp(l)[0]) > 0.2]
links = random.sample(links, min(10, len(links)))
mondo = []
for l in links:
    try:
        link_doc = wikipedia.page(l).summary
        link_doc = nlp(link_doc)
        to_add = get_adj_phrases(link_doc, seed_word)
        mondo.extend(to_add)
        to_print = 'links from %s added.  Ex: A %s with %s' %(l, seed_word, to_add[0])
        print(to_print)
    except:
        continue

for el in mondo:
    print('A %s with %s' %(seed_word, el))