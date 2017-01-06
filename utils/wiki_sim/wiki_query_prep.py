import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import shutil
from utils import text_fun 
from gensim import corpora, models


if not os.path.isdir('aux/wiki_model'):
    os.makedirs('aux/wiki_model')
os.chdir('aux/wiki_model')
print(os.getcwd())
titles_path = 'titles.txt'
articles_path = 'articles.txt'
dict_path = 'wiki_dictionary.dict'
corpus_path = 'wiki_corpus.mm'
corpus_lsi_path = 'wiki_corpus_lsi.mm'
lsi_path = 'wiki_lsi.lsi'
index_prefix = 'index_shards/wiki_index'
index_path = 'index_shards/lsi_wiki_index.index'


folders = os.listdir('../wiki_html')
folders = ['../wiki_html/' + f for f in \
    folders if os.path.isdir('../wiki_html/' + f)]

# process files 
for folder in folders:
    folder_files = os.listdir(folder)
    folder_files = [f for f in folder_files if not \
        f.startswith('.')]
    for file in folder_files:
        if file.startswith('wiki'):
            input_path = folder + '/' + file
            titles_path = folder + '/' + 'titles_' + file
            articles_path = folder + '/' + 'articles_' + file
            text_fun.prep_save(input_path, titles_path, 
                articles_path)
            print('%s/%s processed.' %(folder, file))

# save titles.txt
if os.path.isfile(titles_path):
    print('Titles file found on disk at', titles_path)
with open('titles.txt', 'wb') as f:
    for folder in folders:
        print(folder)
        folder_files = os.listdir(folder)
        folder_files = [f for f in folder_files if not \
            f.startswith('.')]
        for file in folder_files:
            if file.startswith('titles_'):
                input_path = folder + '/' + file
                with open(input_path, 'rb') as f_sub:
                    shutil.copyfileobj(f_sub, f) 

# save articles.txt
if os.path.isfile(articles_path):
    print('Articles file found on disk at', articles_path)
else:
    with open('articles.txt', 'wb') as f:
        for folder in folders:
            print(folder)
            folder_files = os.listdir(folder)
            folder_files = [f for f in folder_files if not \
                f.startswith('.')]
            for file in folder_files:
                if file.startswith('articles_'):
                    input_path = folder + '/' + file
                    with open(input_path, 'rb') as f_sub:
                        shutil.copyfileobj(f_sub, f) 


# dictionary .............................................
if not os.path.isfile(dict_path):
    print('Dictionary not found.  Creating one...')
    line_factory = text_fun.line_streamer(articles_path, N)
    id2word = corpora.Dictionary(text_fun.line_streamer(articles_path, 
                                                        N))
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
    corpus = text_fun.WikiCorpus(articles_path, id2word, N) 
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