# This script needs a gensim corpus, an associated gensim dictionary, and
# an associated gensim lsi (or lda) model to work. In what follows,
# 'Aux/wiki_en_tfidf.mm' is a gensim corpus saved on disk in market matrix format,
# 'wiki_en_wordids.txt' is the associated dictionary,
# and 'wiki_en_lsi' is the the associated lsi model.

import os
import gensim
import sys

os.chdir(os.getenv('HOME') + '/Documents/Blender/Aux/wiki_model')

# Load a previously created corpus in lsi format
lsiCorpus = gensim.corpora.MmCorpus('wiki_corpus_lsi.mm')

# Loads a previously created dictionary 
id2word = gensim.corpora.Dictionary.load('wiki_dictionary.dict')

# Loads a pre-computed lsi model named 'wiki_lsi'.  
# Type str(lsi) for basic info.
lsi = gensim.models.LsiModel.load('wiki_lsi')


doc = """
A skateboard is a type of sports equipment used primarily for the activity of skateboarding. It usually consists of a specially designed maplewood board combined with a polyurethane coating used for making smoother slides and stronger durability. Most skateboards are made with 7 plies of this wood.

A skateboard is moved by pushing with one foot while the other remains on the board, or by pumping one's legs in structures such as a bowl or half pipe. A skateboard can also be used by simply standing on the deck while on a downward slope and allowing gravity to propel the board and rider. If the rider positions their right foot forward, he/she is said to ride "goofy;" if the rider positions their left foot forward, he/she is said to ride "regular." If the rider is normally regular but chooses to ride goofy, he/she is said to be riding in "switch," and vice versa. A skater is typically more comfortable pushing with their back foot; choosing to push with the front foot is commonly referred to as riding "mongo", and has negative connotations of style and effectiveness in the skateboarding community.

Recently, electric skateboards have also appeared. These no longer require the propelling of the skateboard by means of the feet; rather an electric motor propels the board, fed by an electric battery.

There is no governing body that declares any regulations on what constitutes a skateboard or the parts from which it is assembled. Historically, the skateboard has conformed both to contemporary trends and to the ever-evolving array of stunts performed by riders/users, who require a certain functionality from the board. Of course, the board shape depends largely upon its desired function. Longboards are a type of skateboard with a longer wheelbase and larger, softer wheels.

The two main types of skateboards are the longboard and the shortboard. The shape of the board is also important: the skateboard must be concaved to perform tricks.[1] Longboards are usually faster and are mostly used for cruising and racing, while shortboards are mostly used for doing tricks
"""

# Split doc, change to BOW (bag of words) and translate to lsi space 
lsiString = lsi[id2word.doc2bow(doc.split())]

#--------------------------------------------------------------------------
# Comment this block out if you already have lsiWikiIndex.index,
# since otherwise it will take some major time
#--------------------------------------------------------------------------

# Takes a corpus (lsiCorpus in this case), and creates a document index.
# Basically represents the documents in lsi space. The documents are stored
# to disk as a series of 'shards'. The shards have the prefix lsiWikiIndex
# and are stored in './Aux'.  
index =
    gensim.similarities.docsim.Similarity('./index_shards/wiki_index',
        lsiCorpus, num_features = lsi.num_topics, num_best = 30)
# Save the index 
index.save('lsi_wiki_index.index')

#--------------------------------------------------------------------------

# Load the index
index = gensim.similarities.docsim.Similarity.load(
    './Aux/indexShards/lsiWikiIndex.index'
    )

similar = index[lsiString]

# docNumber is the index of the document from the corpus which is closest
# to the query in lsi space.  
docNumber = similar[0][0]
print(docNumber)
