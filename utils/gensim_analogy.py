import os
os.chdir(os.getenv('HOME') + '/Desktop')
from gensim.models import KeyedVectors
import gensim.downloader as api


gw300 = api.load('glove-wiki-gigaword-300')
print(gw300.most_similar(positive=['woman', 'king'], negative=['man']))