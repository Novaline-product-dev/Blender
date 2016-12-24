import os
import gensim
import sys
import wikipedia
os.chdir(os.getenv('HOME') + '/Documents/Blender/Utilities')
import text_fun
os.chdir(os.getenv('HOME') + '/Documents/Blender/Aux/wiki_model')


query_term = 'spatula'

# Load a previously created corpus in lsi format
lsiCorpus = gensim.corpora.MmCorpus('wiki_corpus_lsi.mm')

# Loads a previously created dictionary 
id2word = gensim.corpora.Dictionary.load('wiki_dictionary.dict')

# Loads a pre-computed lsi model named 'wiki_lsi'.  
lsi = gensim.models.LsiModel.load('wiki_lsi')

# Load the index
index = gensim.similarities.docsim.Similarity.load('./index_shards/lsi_wiki_index.index')


doc = wikipedia.page(query_term).content
doc = text_fun.prune(doc) 
lsiString = lsi[id2word.doc2bow(doc)]
similar = index[lsiString]
 
docNumber = similar[0][0]
with open('titles.txt', 'rb') as f:
	titles = f.readlines()
for element in similar:
	print(titles[element[0]])