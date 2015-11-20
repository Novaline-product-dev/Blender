import pickle
import os
import numpy as np 
import scipy as sp 
import pandas as pd 
import nltk
from sklearn.feature_extraction import text 
from nltk.corpus import stopwords

os.chdir(os.getenv('HOME') + '/Documents/Blender')
textList = pickle.load( open("output.p", "rb"))

# May want to move to a separate file with helper functions
def hasNumber(string):
	if any(char.isdigit() for char in string):
		return(True)
	else:
		return(False)

for i, doc in enumerate(textList):
	temp = doc.split()
	temp = [w for w in temp if w not in stopwords.words('english')]
	temp = [w for w in temp if not hasNumber(w)]
	textList[i] = ' '.join(temp)

vectorizer = text.CountVectorizer()
dtm = vectorizer.fit_transform(textList)
dtm = dtm.toarray()
vocab = vectorizer.get_feature_names()
ranks = ['Rank %d' %(i + 1) for i in range(dtm.shape[0])]
dtm = pd.DataFrame(dtm, index = ranks, columns = vocab)

# Remove columns corresponding to words that have numbers
for i, string in enumerate(vocab): 
	check = any(char.isdigit() for char in string)
	if check: del dtm[string] 


# Crossproduct of document-term matrix with itself
ttm = np.dot(dtm.transpose(), dtm) # term-term matrix, or adjacency matrix