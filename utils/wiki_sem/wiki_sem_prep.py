import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import gzip
import shutil
from utils import text_fun 
from gensim import corpora, models, similarities


if not os.path.isdir('aux/wiki_model'):
    os.makedirs('aux/wiki_model')
os.chdir('aux/wiki_model')
print(os.getcwd())
sentences_path = 'depency_sentences.txt'

folders = os.listdir('../wiki_html')
folders = ['../wiki_html/' + f for f in \
    folders if os.path.isdir('../wiki_html/' + f)]

# process files 
for folder in folders:
    folder_files = os.listdir(folder)
    folder_files = [f for f in folder_files if \
        f.startswith('wiki_')]
    for file in folder_files:
        input_path = folder + '/' + file
        sentenc_path = folder + '/' + 'dependency_sentences_' + file
        text_fun.prep_save_sem(input_path, sentenc_path)
        print('%s/%s processed.' %(folder, file))

if os.path.isfile(sentences_path + '.gz'):
    print('Dependency sentences file found on disk at', )
else:
    with gzip.open(sentences_path + '.gz', 'wb') as f:
        for folder in folders:
            print(folder)
            folder_files = os.listdir(folder)
            folder_files = [f for f in folder_files if \
                f.startswith('dependency')]
            for file in folder_files:
                to_add = folder + '/' + file
                with open(to_add, 'rb') as f_sub:
                    shutil.copyfileobj(f_sub, f) 

sentences = models.word2vec.LineSentence(sentences_path + '.gz')
sem_model = models.word2vec.Word2Vec(sentences, size=300, window=5, 
    min_count=8, workers=3, sg=1, negative=10)
sem_model.save('wiki_sem_w2v')