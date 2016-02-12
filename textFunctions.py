import string
import re
from scipy import stats
import numpy as np
from numpy import *
import pandas as pd
from statsmodels.distributions import empirical_distribution as ed 

def hasNumber(stringToCheck):
	return bool(re.search(r'\d', stringToCheck))

def rmPunct(dirtyStr):
	splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
	cleanStr = ''.join(splitCleanStr)
	return(cleanStr)

def cdf(array):
	array = np.array(array)
	utVec = np.diagonal(array)
	for i in range(1, array.shape[0]):
		utVec = np.concatenate([utVec, np.diagonal(array, i)])
	xgrid = np.linspace(0, 1, 500)
	ecdf = ed.ECDF(utVec)
	yvals = ecdf(xgrid)
	return(yvals)

def ks(cdfVec1, cdfVec2):
	return(max(abs(cdfVec1 - cdfVec2)))