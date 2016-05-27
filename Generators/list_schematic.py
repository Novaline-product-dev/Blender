import os, string, wikipedia
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Utilities')
import text_fun
import nltk
from nltk import word_tokenize


textList = pickle.load( open("../fulltext.p", "rb"))
textList = [text_fun.prune(doc) for doc in textList]

ksEvaluator = ksFunctions.ksFunctionGenerator(textList)


header = wikipedia.summary("3D printing")
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = sent_detector.tokenize(header.strip())
tokens = set(word_tokenize(header))
for token in tokens:
