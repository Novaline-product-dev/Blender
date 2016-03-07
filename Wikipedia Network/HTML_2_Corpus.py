## Processes the HTML-format file of all Wikipedia articles

import sys
sys.path.append("..")
import textFunctions as tf
from gensim import corpora, models
from lxml import html


def textractor(file):
    """Accesses the text of documents in an html file (returns a list)."""
    raw_text = []
    with open(file) as f:
        soup = html.fromstring(f.read())
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def titlextractor(file):
    """Accesses the title of documents in an html file (returns a list)."""
    titles=[]
    with open(file) as f:
        soup = html.fromstring(f.read())
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles


# Provide a route by which to access all the files (it's just one right now)
files = ['Example_wiki_html_short.txt']


# Run through each file at a time, collecting stats about tokens
# Weird list comprehension: http://stackoverflow.com/ ...
# questions/1198777/double-iteration-in-list-comprehension
# Try reading it from bottom to top
dictionary = corpora.Dictionary(
    tf.prune(doc)
        for file in files
            for doc in textractor(file))
# Remove frequent and infrequent words, and limit tokens to 100,000
dictionary.filter_extremes(no_below = 0)  # Remove no_below for large dictionary
dictionary.compactify()


# Create a corpus using the previous dictionary and all the files
# This only holds one file in memory at a time.
class MyCorpus(object):
    def __iter__(self):
        for file in files:
            titles = titlextractor(file)
            docs = textractor(file)
            for title, doc in zip(titles, docs):
                with open('titles.txt', 'a') as f:      # This may not be the most memory-efficient. Research it
                    f.write(''.join((title, '\n')))
                f.close()
                yield dictionary.doc2bow(tf.prune(doc))


corpus = MyCorpus()

# For debugging:
##for vector in corpus:
##    print(vector)
    
# Convert the corpus to Market Matrix format and save it.
corpora.MmCorpus.serialize('testcorpus.mm', corpus)
# To load this corpus, use corpus = corpora.MmCorpus('testcorpus.mm')
