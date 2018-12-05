import wikipedia
import random
import spacy
from spacy.symbols import amod


nlp = spacy.load('en')
seed = 'radio'
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
            el_str = el.lemma_
            more_or_less = random.choice(['more', 'less'])
            if el.similarity(seed_word) > 0.1:
                out.append('that is %s %s' % (more_or_less, el_str))
                out.append('+ ' + str(el).lower() + ' ' +  \
                    str(el.head).lower())
    return out

def get_action_phrases(doc, word):
    out = []
    for el in doc:
        if el.dep_ == 'nsubj':
            if el.similarity(word) > 0.1:
                for child in el.head.children:
                    if child.dep_ == 'dobj':
                        out.append('where ' + str(el).lower() + ' ' + \
                        str(el.head).lower() + ' ' + str(child).lower())

    return out

links = [l for l in page.links if seed_word.similarity(nlp(l)[0]) > 0.2]
links = random.sample(links, min(30, len(links)))
mondo = []
for l in links:
    try:
        link_doc = wikipedia.page(l).summary
        link_doc = nlp(link_doc)
        to_add1 = get_adj_phrases(link_doc, seed_word)
        to_add2 = get_action_phrases(link_doc, seed_word)
        mondo.extend(to_add1)
        mondo.extend(to_add2)
        to_print = 'links from %s added.' %l
        print(to_print)
    except:
        continue

seen = set()
for el in mondo:
    el_idea = 'A %s %s' %(seed_word, el)
    if el_idea not in seen:
        print(el_idea)
        seen.add(el_idea)