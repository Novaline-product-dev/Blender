import wikipedia
from spacy.en import English
from spacy.symbols import amod


nlp = English()
a = wikipedia.page('pen')
doc = a.content
doc = nlp(doc)
pen = nlp('pen')[0]

def get_adj_phrases(doc, word):
    out = []
    for el in doc:
        if el.dep_ == 'amod':
            if el.similarity(word) > 0.2:
                out.append(str(el) + ' ' + str(el.head))
    return out

links = [l for l in a.links if pen.similarity(nlp(l)[0]) < 0.3]
mondo = []
for l in links:
    try:
        link_doc = wikipedia.page(l).summary
        link_doc = nlp(link_doc)
        to_add = get_adj_phrases(link_doc, pen)
        mondo.extend(to_add)
        to_print = 'links from %s added.  Ex: A pen with %s' %(l, to_add[0])
        print(to_print)
    except:
        continue

for el in mondo:
    print('A pen with %s' %el)