import sys
sys.path.append('../../Utilities')
import os
import text_fun as tf
from gensim import corpora, models
from lxml import html
from datetime import datetime
os.chdir('../../Aux/wiki_html')

def time():
    return str(datetime.now())[5:19]

def textractor(file_name):
    """Accesses the text of documents in an html file (returns a list)."""
    raw_text = []
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def titlextractor(file_name):
    """Accesses the title of documents in an html file (returns a list)."""
    titles=[]
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

print(time(), 'Start.')
files = []
# filenames.txt is output of filename_list_generator.py
with open('../../Utilities/wiki_sim/filenames.txt', 'r') as f:
    for line in f:
        files.append(line.strip('\n'))
print(time(), 'Filenames Read.  For example, the first file is:', files[0])
print('The current working directory is', os.getcwd())

print(time(), 'Beginning to load dictionary.')
dictionary = corpora.Dictionary(
    tf.prune(doc)
        for file_name in files
            for doc in textractor(file_name))
print(time(), 'Dictionary loaded. Filtering extremes.')

## Remove frequent and infrequent words, and limit tokens to 100,000
dictionary.filter_extremes()
dictionary.compactify()
os.chdir('../wiki_model')
dictionary.save('wiki_dictionary.dict')

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
    
print(time(), 'Corpus built. Converting to Market Matrix format.')
corpora.MmCorpus.serialize('wiki_corpus.mm', corpus)
print(time(), 'Market Matrix format saved. Process finished.')


print('Loading corpus...')
mmcorpus = corpora.MmCorpus('wiki_corpus.mm')
print('Wikipedia Corpus Loaded')

#print('Creating TFIDF model...')
#tfidf = models.TfidfModel(mmcorpus) 
#print('TFIDF model created')

#print('Transforming corpus to TFIDF...')
#mmcorpus_tfidf = tfidf[mmcorpus]
#corpora.MmCorpus.serialize('corpus_tfidf.mm', mmcorpus_tfidf)
#print('TFIDF corpus saved')

print('Creating LSI Model...')
dictionary=corpora.Dictionary.load('wiki_dictionary.dict')
lsi = models.LsiModel(mmcorpus, id2word=dictionary, num_topics=400, decay=1.0, chunksize=20000)
lsi.print_topics(2)
lsi.save('wiki_lsi')

print('Transforming Wikipedia Corpus to LSI')
mmcorpus_lsi = lsi[mmcorpus]
corpora.MmCorpus.serialize('wiki_corpus_lsi.mm', mmcorpus_lsi)
print('Corpus transformed to LSI space.')

print('Creating index...')
index = gensim.similarities.docsim.Similarity('./index_shards/wiki_index',
        lsiCorpus, num_features = lsi.num_topics, num_best = 30)
index.save('./index_shards/lsi_wiki_index.index')
print('Done!')
