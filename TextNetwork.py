import pickle
import os
import numpy as np 
import scipy as sp 
import pandas as pd 
import nltk
import string
from sklearn.feature_extraction import text 
from nltk.corpus import stopwords

os.chdir(os.getenv('HOME') + '/Documents/Blender')
textList = pickle.load( open("output.p", "rb"))

# May want to move to a separate file with other helper functions
def hasNumber(stringToCheck):
	if any(char.isdigit() for char in stringToCheck):
		return(True)
	else:
		return(False)

def rmPunct(dirtyStr):
	splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
	cleanStr = ''.join(splitCleanStr)
	return(cleanStr)

myExcludes = set(['[', ']', '\'', '\n'])
for i, doc in enumerate(textList):
	temp = doc.split() # split text into a list at spaces
	
	# remove words with numbers
	temp = [w for w in temp if not hasNumber(w)]

	# remove freestanding punctuation, and punctuation in words
	temp = [w for w in temp if w not in string.punctuation]
	temp = [rmPunct(w) for w in temp]
	
	# remove characters specified by me
	temp = [w for w in temp if w not in myExcludes]

	# remove stopwords.  nltk is case-sensitive: use lowercase.  This step has to be done last, after removing punctuation, etc.
	temp = [w for w in temp if w.lower() not in stopwords.words('english')]

	# reversing the split performed above
	textList[i] = ' '.join(temp)


vectorizer = text.CountVectorizer()
dtm = vectorizer.fit_transform(textList)
dtm = dtm.toarray()
vocab = vectorizer.get_feature_names()
ranks = ['Rank %d' %(i + 1) for i in range(dtm.shape[0])]
dtm = pd.DataFrame(dtm, index = ranks, columns = vocab)

# Crossproduct of document-term matrix with itself
ttm = np.dot(dtm.transpose(), dtm) # term-term matrix, or adjacency matrix