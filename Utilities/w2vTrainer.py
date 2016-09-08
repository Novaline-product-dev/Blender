import os, bz2
import nltk


sentenceDetector = nltk.data.load('tokenizers/punkt/english.pickle')
# Now the script converts the files from bz2 to txt and then trains on the 
# txt files.  However, it would be good to write sentenceFactory to use
# bz2 files instead.  Just do it later.

#### Step 1: convert bz2 files to txt files
# Directory with the files
os.chdir(os.getenv('HOME') + '/Documents/Blender/Aux')
dirpath = './extracted/AA'
files = os.listdir(dirpath)
files = [file for file in files if file.endswith('.bz2')]
for filename in files:
    filepath = os.path.join(dirpath, filename) # to get compressed file
    newfilepath = os.path.join(dirpath, filename[:-4] + '.txt') # for output files
    
    with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        for data in iter(lambda : file.read(), b''):
            new_file.write(data)



##### Processing and training for one file

with open('./extracted/AA/wiki_00.txt', 'r', encoding = 'utf-8') as f:
	stringList = f.readlines()

docInd = 0
for i, item in enumerate(stringList):
	if docInd:
		stringList.remove(item)
	docInd = item.startswith('<doc id')
	if docInd:
		stringList.remove(item)

stringList = [el for el in stringList if ' ' in el]

# This currently leaves periods at the end of the sentence
stringList = [sentenceDetector.tokenize(el) for el in stringList]




# Build the sentence generator

#class sentenceFactory(object):
#    def __init__(self, dirname):
#        self.dirname = dirname
# 
#    def __iter__(self):
#    	fnames = os.listdir(self.dirname)
#        for fname in fnames:
#            
#            for line in open(os.path.join(self.dirname, fname)):
#                yield line.split()

#sentences = sentenceFactory('/some/directory') # a memory-friendly iterator
#model = gensim.models.Word2Vec(sentences)