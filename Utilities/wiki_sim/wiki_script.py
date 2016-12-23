import os
import gensim
import sys
import wikipedia
os.chdir(os.getenv('HOME') + '/Documents/Blender/Utilities')
import text_fun
os.chdir(os.getenv('HOME') + '/Documents/Blender/Aux/wiki_model')


# Load a previously created corpus in lsi format
lsiCorpus = gensim.corpora.MmCorpus('wiki_corpus_lsi.mm')

# Loads a previously created dictionary 
id2word = gensim.corpora.Dictionary.load('wiki_dictionary.dict')

# Loads a pre-computed lsi model named 'wiki_lsi'.  
# Type str(lsi) for basic info.
lsi = gensim.models.LsiModel.load('wiki_lsi')


#--------------------------------------------------------------------------
# Comment this block out if you already have lsiWikiIndex.index,
# since otherwise it will take some major time
#--------------------------------------------------------------------------

# Takes a corpus (lsiCorpus in this case), and creates a document index.
# Basically represents the documents in lsi space. The documents are stored
# to disk as a series of 'shards'. The shards have the prefix lsiWikiIndex
# and are stored in './Aux'.  
#index = gensim.similarities.docsim.Similarity('./index_shards/wiki_index',
#        lsiCorpus, num_features = lsi.num_topics, num_best = 30)
# Save the index 
#index.save('./index_shards/lsi_wiki_index.index')

#--------------------------------------------------------------------------

# Load the index
index = gensim.similarities.docsim.Similarity.load('./index_shards/lsi_wiki_index.index')


doc = wikipedia.page('skateboard').content
doc = text_fun.prune(doc)
# Split doc, change to BOW (bag of words) and translate to lsi space 
lsiString = lsi[id2word.doc2bow(doc)]

similar = index[lsiString]

# docNumber is the index of the document from the corpus which is closest
# to the query in lsi space.  
docNumber = similar[0][0]
with open('titles.txt', 'rb') as f:
	titles = f.readlines()
for element in similar:
	print(titles[element[0]])