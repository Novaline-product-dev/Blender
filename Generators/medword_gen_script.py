import pickle, os, string, random, statistics
UtilPath = os.getenv('HOME') + '/Documents/Blender/Utilities'
os.chdir(UtilPath)
import text_fun
os.chdir(os.getenv('HOME') + '/Documents/Blender/Generators')
import medword
os.chdir(os.getenv('HOME') + '/Documents/Blender')

import numpy as np 
import pandas as pd
import nltk
import enchant
from gensim import corpora, models, similarities, utils

print(' '.join(medword.median_words('..')))

# Plot.  Comment if you don't care.
#--------------------------------------------------------------------
#text_fun.textNetworkPlot(textList)
