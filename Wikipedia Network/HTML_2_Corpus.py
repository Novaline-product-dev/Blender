## Processes the HTML-format file of all Wikipedia articles
## Line 42 needs to be changed to access your articles in HTML form

import sys
sys.path.append("..")
import os
import textFunctions as tf
from gensim import corpora, models
from lxml import html
from datetime import datetime

def time():
    return str(datetime.now())[5:19]

def textractor(file_name):
    """Accesses the text of documents in an html file (returns a list)."""
    raw_text = []
    with open(file_name) as f:
        soup = html.fromstring(f.read())
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def titlextractor(file_name):
    """Accesses the title of documents in an html file (returns a list)."""
    titles=[]
    with open(file_name) as f:
        soup = html.fromstring(f.read())
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

print(time(), 'Start.')
# Provide a route by which to access all the files
os.chdir(os.environ['HOME'])
files = []
# Make sure you have already generated a list of files with
# filename_list_generator.py
with open('Documents/Blender/Wikipedia Network/filenames.txt', 'r') as f:
    for line in f:
        files.append(line.strip('\n'))
os.chdir('wikidump/wiki_html3')  ### THIS IS HARDCODED FOR FSL.byu.edu -
# You can change this to your directory that houses the AA,AB,AC files


# Run through each file at a time, collecting stats about tokens
# Weird list comprehension: http://stackoverflow.com/ ...
# questions/1198777/double-iteration-in-list-comprehension
# Try reading it from bottom to top
print(time(), 'Beginning to load dictionary.')
dictionary = corpora.Dictionary(
    tf.prune(doc)
        for file_name in files
            for doc in textractor(file_name))
dictionary.save('testdictionary.dict')
print(time(), 'Dictionary loaded. Filtering extremes.')
# Remove frequent and infrequent words, and limit tokens to 100,000
dictionary.filter_extremes(no_below = 0)  # Remove no_below for large dictionary
dictionary.compactify()


# Create a corpus using the previous dictionary and all the files
# This only holds one file in memory at a time.
class MyCorpus(object):
    def __iter__(self):
        for i, file_name in enumerate(files):
            if i%10000 == 0 and i != 0:
                print(time(), '%i files added to corpus.' %i)
            titles = titlextractor(file_name)
            docs = textractor(file_name)
            for title, doc in zip(titles, docs):
                with open('titles.txt', 'a') as f:
                    f.write(''.join((title, '\n')))
                yield dictionary.doc2bow(tf.prune(doc))

print(time(), 'Building corpus.')
corpus = MyCorpus() 

# For debugging:
##for vector in corpus:
##    print(vector)
    
# Convert the corpus to Market Matrix format and save it.
print(time(), 'Corpus built. Converting to Market Matrix format.')
corpora.MmCorpus.serialize('testcorpus.mm', corpus)
print(time(), 'Market Matrix format saved. Process finished.')

"""The following will set everything up to use wikiScript to make comparisons.
wikiScript.py requires a tfidfcorpus (testcorpus_tfidf.mm, see below),
a dictionary (testdictionary.dict, see above), and an lsi model
(testcorpus_lsi.mm). This is probably best done from the shell as each of these
steps will take a very long time. However, this section can be uncommented out
for testing on smaller sets of documents."""

### Load the Market Matrix corpus
##mmcorpus = corpora.MmCorpus('testcorpus.mm')
### Create the tfidf model object
##tfidf = models.TfidfModel(mmcorpus)
### Transform the whole corpus and save it
##mmcorpus_tfidf = tfidf[mmcorpus]
##corpora.MmCorpus.serialize('testcorpus_tfidf.mm', mmcorpus_tfidf)
### Create the lsi model object
##dictionary=corpora.Dictionary.load('testdictionary.dict')
##lsi = models.LsiModel(mmcorpus, id2word=dictionary, num_topics=2)
##lsi.print_topics(2)
### Transform the whole corpus and save it
##mmcorpus_lsi = lsi[mmcorpus]
##corpora.MmCorpus.serialize('testcorpus_lsi.mm', mmcorpus_lsi)

