import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import shutil
from utils import text_fun 
from gensim import corpora, models, similarities


if not os.path.isdir('aux/wiki_model'):
    os.makedirs('aux/wiki_model')
os.chdir('aux/wiki_model')
print(os.getcwd())
sentences_path = 'sentences.txt'

folders = os.listdir('../wiki_html')
folders = ['../wiki_html/' + f for f in \
    folders if os.path.isdir('../wiki_html/' + f)]

def article_gen(folders):
    for folder in folders:
        folder_files = os.listdir(folder)
        folder_files = [f for f in folder_files if not \
            f.startswith('.')]
        for file in folder_files:
            if file.startswith('wiki'):
                articles = text_fun.text_extractor(folder + '/' + file)
                for article in articles:
                    yield article

# process files 
for folder in folders:
    folder_files = os.listdir(folder)
    folder_files = [f for f in folder_files if not \
        f.startswith('.')]
    for file in folder_files:
        if file.startswith('wiki'):
            input_path = folder + '/' + file
            sentenc_path = folder + '/' + 'sentences_' + file
            text_fun.prep_save_w2v(input_path, sentenc_path)
            print('%s/%s processed.' %(folder, file))

# save articles.txt
#if os.path.isfile(articles_path):
#    print('Articles file found on disk at', articles_path)
#else:
#    with open('articles.txt', 'wb') as f:
#        for folder in folders:
#            print(folder)
#            folder_files = os.listdir(folder)
#            folder_files = [f for f in folder_files if not \
#                f.startswith('.')]
#            for file in folder_files:
#                if file.startswith('articles_'):
#                    input_path = folder + '/' + file
#                    with open(input_path, 'rb') as f_sub:
#                        shutil.copyfileobj(f_sub, f) 
#
#with open(titles_path, 'rb') as f:
#    for i, l in enumerate(f):
#        pass
#    N = i + 1
#
## dictionary .............................................
#if not os.path.isfile(dict_path):
#    print('Dictionary not found.  Creating one...')
#    line_factory = text_fun.line_streamer(articles_path, N)
#    id2word = corpora.Dictionary(text_fun.line_streamer(articles_path, 
#                                                        N))
#    print('Dictionary created. Filtering extremes.')
#    id2word.filter_extremes()
#    id2word.compactify()
#    id2word.save(dict_path)
#    print('Dictionary saved.')
#
#print('Loading dictionary from disk...')
#id2word = corpora.Dictionary.load(dict_path)
#print('Dictionary loaded.')
## end dictionary .............................................
#
## corpus......................................................
#if not os.path.isfile(corpus_path):
#    print('Corpus not found.  Creating one...')
#    corpus = text_fun.WikiCorpus(articles_path, id2word, N) 
#    print('Corpus created. Saving to Market Matrix format.')
#    corpora.MmCorpus.serialize(corpus_path, corpus)
#    print('Corpus saved to disk.')
#
#print('Loading corpus...')
#mmcorpus = corpora.MmCorpus(corpus_path)
## end corpus..................................................
#
#dictionary=corpora.Dictionary.load(dict_path)
#
#if not os.path.isfile(lsi_path):
#    print('Creating LSI Model...')
#    lsi = models.LsiModel(mmcorpus, id2word=dictionary, 
#        num_topics=400, decay=1.0, chunksize=20000)
#    print('LSI model created. First two topics:')
#    print(lsi.print_topics(2))
#    lsi.save(lsi_path)
#else:
#    lsi = models.LsiModel.load(lsi_path)
#
#if not os.path.isfile(corpus_lsi_path):
#    print('Transforming Wikipedia Corpus to LSI')
#    mmcorpus_lsi = lsi[mmcorpus]
#    corpora.MmCorpus.serialize(corpus_lsi_path, mmcorpus_lsi)
#
#print('Loading LSI corpus...')
#lsiCorpus = corpora.MmCorpus(corpus_lsi_path)
#
#if not os.path.isfile(index_path):
#    if not os.path.isdir(index_dir):
#        os.makedirs(index_dir)
#    print('Creating index...')
#    index = similarities.docsim.Similarity(index_prefix,
#        lsiCorpus, num_features=lsi.num_topics, num_best=30)
#    index.save(index_path)
#print('Done!')#