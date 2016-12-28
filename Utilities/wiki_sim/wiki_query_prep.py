import sys
sys.path.append('..')
import os
import text_fun 
from gensim import corpora, models
from lxml import html
from datetime import datetime
os.chdir('../../Aux/wiki_html')


files = []
directory_list = os.listdir()
for directory in directory_list:
    for file in os.listdir(directory):
        files.append(directory + '/' + file)

model_path = '../wiki_model'
if not os.path.isdir(model_path):
    os.makedirs(model_path)

# dictionary .............................................
dict_path = '../wiki_model/wiki_dictionary.dict'
if not os.path.isfile(dict_path):
    print('Dictionary not found.  Creating one...')
    id2word = corpora.Dictionary(
        text_fun.prune(doc)
            for file_name in files
                for doc in text_fun.text_extractor(file_name))
    print('Dictionary created. Filtering extremes.')

    # Remove freq. and infreq. words, limit tokens to 100K
    id2word.filter_extremes()
    id2word.compactify()
    id2word.save(dict_path)
    print('Dictionary saved.')

print('Loading dictionary from disk...')
id2word = corpora.Dictionary.load(dict_path)
print('Dictionary loaded.')
# end dictionary .............................................
# corpus......................................................
corpus_path = '../wiki_model/wiki_corpus.mm'
if not os.path.isfile(corpus_path):
    print('Corpus not found.  Creating one...')
    titles_path = '../wiki_model/titles.txt'
    corpus = text_fun.WikiCorpus(titles_path, files, id2word) 
    if not os.path.isfile(titles_path):
        corpus.save_titles(titles_path)
    
    print('Corpus created. Saving to Market Matrix format.')
    corpora.MmCorpus.serialize(corpus_path, corpus)
    print('Corpus saved to disk.')

print('Loading corpus...')
mmcorpus = corpora.MmCorpus(corpus_path)
# end corpus..................................................

os.chdir(model_path)
print('Creating LSI Model...')
dictionary=corpora.Dictionary.load('wiki_dictionary.dict')
lsi = models.LsiModel(mmcorpus, id2word=dictionary, num_topics=400, 
                      decay=1.0, chunksize=20000)
lsi.print_topics(2)
lsi.save('wiki_lsi')

print('Transforming Wikipedia Corpus to LSI')
mmcorpus_lsi = lsi[mmcorpus]
corpora.MmCorpus.serialize('wiki_corpus_lsi.mm', mmcorpus_lsi)

print('Creating index...')
index = gensim.similarities.docsim.Similarity('./index_shards/wiki_index',
        lsiCorpus, num_features=lsi.num_topics, num_best=30)
index.save('./index_shards/lsi_wiki_index.index')
print('Done!')