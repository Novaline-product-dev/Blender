import sys
sys.path.append('..')
import os
import text_fun 
from gensim import corpora, models
from lxml import html
from datetime import datetime
os.chdir('../../Aux/wiki_html')

def time():
    return str(datetime.now())[5:19]

files = []
# filenames.txt is output of filename_list_generator.py
with open('../../Aux/wiki_model/filenames.txt', 'r') as f:
    for line in f:
        files.append(line.strip('\n'))
print(time(), 'Filenames Read.  For example, the first file is:', files[0])
print('The current working directory is', os.getcwd())


# dictionary .............................................
dict_path = '../wiki_model/wiki_dictionary.dict'
if not os.path.isfile(dict_path):
    print('Dictionary not found.')
    print(time(), 'Beginning to create dictionary.')
    gensim_dictionary = corpora.Dictionary(
        text_fun.prune(doc)
            for file_name in files
                for doc in textractor(file_name))
    print(time(), 'Dictionary loaded. Filtering extremes.')

    ## Remove frequent and infrequent words, and limit tokens to 100,000
    gensim_dictionary.filter_extremes()
    gensim_dictionary.compactify()
    gensim_dictionary.save(dict_path)

print('Loading dictionary from disk.')
gensim_dictionary = corpora.Dictionary.load(dict_path)
print('Dictionary loaded.')
# end dictionary .............................................


# corpus......................................................
corpus_path = '../wiki_model/wiki_corpus.mm'
if not os.path.isfile(corpus_path):
    print('Corpus not found.')
    print(time(), 'Building corpus.')
    titles_path = '../wiki_model/titles.txt'
    corpus = WikiCorpus(titles_path, files) 
    if not os.path.isfile(titles_path):
        corpus.save_titles(titles_path)
    
    print(time(), 'Corpus built. Saving in Market Matrix format.')
    corpora.MmCorpus.serialize(corpus_path, corpus)
    print(time(), 'Corpus saved in Market Matrix format.')

print('Loading corpus...')
mmcorpus = corpora.MmCorpus(corpus_path)
print('Wikipedia Corpus Loaded')
# end corpus..................................................

os.chdir('../wiki_model')
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
