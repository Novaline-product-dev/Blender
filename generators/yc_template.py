import os, sys, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils import yc_data_gen
from numpy.random import choice
import spacy
import requests
import random
import pandas as pd
import urllib
from bs4 import BeautifulSoup as BS



if os.path.isfile('yc_objs.p'):
	with open('yc_objs.p', 'rb') as f:
		objs = pickle.load(f)
else:
	yc_data_gen.yc_scrape()
	with open('yc_objs.p', 'rb') as f:
		objs = pickle.load(f)
descriptions = objs[0]
targets = objs[1]
ranks1 = objs[2]
ranks2 = objs[3]

def generate():
    entity = choice(ranks1, 1, p=ranks2)[0]
    print(entity, 'for', random.choice(targets))
    description = [d[1] for d in descriptions if d[0] == entity]
    print('%s: %s' % (entity , description[0]))

generate()
