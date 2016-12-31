import sys
sys.path.append('..')
import os, shutil
import text_fun 
from gensim import corpora, models
from lxml import html
from datetime import datetime


if not os.path.isdir('../../Aux/wiki_model'):
    os.makedirs('../../Aux/wiki_model')
os.chdir('../../Aux/wiki_model')
titles_path = 'titles.txt'
articles_path = 'articles.txt'
dict_path = 'wiki_dictionary.dict'
corpus_path = 'wiki_corpus.mm'
corpus_lsi_path = 'wiki_corpus_lsi.mm'
lsi_path = 'wiki_lsi.lsi'
index_prefix = 'index_shards/wiki_index'
index_path = 'index_shards/lsi_wiki_index.index'

folders = ['../wiki_html/' + f for f in os.listdir() \
    if os.path.isdir(f)]

text_fun.save_titles(folders, titles_path)
text_fun.save_articles(folders, articles_path)

# dictionary .............................................
if not os.path.isfile(dict_path):
    print('Dictionary not found.  Creating one...')
    id2word = corpora.Dictionary(line_streamer(articles_path))
    print('Dictionary created. Filtering extremes.')
    id2word.filter_extremes()
    id2word.compactify()
    id2word.save(dict_path)
    print('Dictionary saved.')

print('Loading dictionary from disk...')
id2word = corpora.Dictionary.load(dict_path)
print('Dictionary loaded.')
# end dictionary .............................................

# corpus......................................................
if not os.path.isfile(corpus_path):
    print('Corpus not found.  Creating one...')
    corpus = text_fun.WikiCorpus(articles_path, id2word) 
    print('Corpus created. Saving to Market Matrix format.')
    corpora.MmCorpus.serialize(corpus_path, corpus)
    print('Corpus saved to disk.')

print('Loading corpus...')
mmcorpus = corpora.MmCorpus(corpus_path)
# end corpus..................................................

print('Creating LSI Model...')
dictionary=corpora.Dictionary.load(dict_path)
lsi = models.LsiModel(mmcorpus, id2word=dictionary, num_topics=400, 
                      decay=1.0, chunksize=20000)
print('LSI model created. First two topics:')
lsi.print_topics(2)
lsi.save(lsi_path)

print('Transforming Wikipedia Corpus to LSI')
mmcorpus_lsi = lsi[mmcorpus]
corpora.MmCorpus.serialize(corpus_lsi_path, mmcorpus_lsi)

print('Creating index...')
index = gensim.similarities.docsim.Similarity(index_prefix,
        lsiCorpus, num_features=lsi.num_topics, num_best=30)
index.save(index_path)
print('Done!')