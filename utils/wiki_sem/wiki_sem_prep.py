import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
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
    folder_files = [f for f in folder_files if not \
        f.startswith('.')]
    for file in folder_files:
        if file.startswith('wiki'):
            input_path = folder + '/' + file
            sentenc_path = folder + '/' + 'dependency_sentences_' + file
            text_fun.prep_save_sem(input_path, sentenc_path)
            print('%s/%s processed.' %(folder, file))