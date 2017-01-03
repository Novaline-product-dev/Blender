import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import gensim
import sys
import wikipedia
from utils import text_fun


os.chdir('aux/wiki_model')
lsiCorpus = gensim.corpora.MmCorpus('wiki_corpus_lsi.mm')
id2word = gensim.corpora.Dictionary.load('wiki_dictionary.dict')
lsi = gensim.models.LsiModel.load('wiki_lsi')
index = gensim.similarities.docsim.Similarity.load('./index_shards/lsi_wiki_index.index')

def similar(query_term):
	dir_on_leave = os.getcwd()
	os.chdir(os.getenv('HOME') + '/Documents/Blender/Aux/wiki_model')
	out = []
	doc = wikipedia.page(query_term).content
	doc = text_fun.prune(doc) 
	lsiString = lsi[id2word.doc2bow(doc)]
	similar = index[lsiString]
	with open('titles.txt', 'rb') as f:
		titles = f.readlines()
	for element in similar:
		out.append(titles[element[0]].decode().strip('\n'))
	out = [el.lower() for el in out]
	out = out[1:]
	os.chdir(dir_on_leave)
	return(out)

os.chdir(os.getenv('HOME') + '/Documents/Blender')
