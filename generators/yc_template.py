import os, sys
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils import spacy_analogy
from numpy.random import choice
import spacy
import requests
import random
import pandas as pd
import urllib
from bs4 import BeautifulSoup as BS


nlp = spacy_analogy.nlp
try:
    yclist 
except NameError:
    r = requests.get('http://yclist.com')
    soup = BS(r.text, 'lxml')
    tbody = soup.tbody
    cos = tbody('tr')
    data_list = [] 
    for co in cos:
        tds = co('td')
        status = co['class'][0]
        if status != 'dead':
            des_el = tds[5]
            span_list = des_el('span')
            if span_list:
                span_list[0].extract()
            data_list.append({
                'Name': tds[1].text.strip(),
                'URL': tds[2].text.strip(),
                'Class': tds[3].text.strip(), 
                'Status': co['class'][0],
                'Description': des_el.text.strip()
                })
    yclist = pd.DataFrame(data_list)

# Maybe remove some junky, ill-formed targets here.  
# Perhaps you should parse the description and use
# appropriate dependencies.  Yes, that's the way to go.
skip = ['hykso', 'meter feeder', 'nurx', 'goodybag',
	'perlara', 'petcube', 'trac', 'worldcover', 
	'flexreceipts', 'pakible', 'paperspace', 'l. international',
	'paribus', 'onboardiq', 'seva coffee', 'redcarpetup',
	'physiohealth', 'greenshoe', 'mtailor', 'shout', 
	'taplytics', 'airbnb', 'agilediagnosis', 'auctomatic',
	'clearbanc', 'panorama education', 'circuitlab',
	'inklingmarkets', 'careskore', 'the flex company',
	'compose', 'isono health', 'givemetap']
targets = []
for i, row in yclist.iterrows():
	description = row['Description'].lower()
	name = row['Name'].lower()
	if (description.find(name) == -1) and (name not in skip): 
	    for_ind = description.find('for ')
	    if for_ind != -1:
	        end = description.find('.')
	        if end == -1:
	            targets.append(description[for_ind + 4:])
	        else:
	            targets.append(description[for_ind + 4:end])

drop = ['for you', 'for all']
targets = [t for t in targets if len(nlp(t)) < 6]
targets = [t for t in targets if t not in drop]
targets = [t for t in targets if t != 'for you']
targets = [t for t in targets if t.find('your ') == -1]
targets = [t for t in targets if t]
targets = list(set(targets))
[print(t) for t in targets]

targets2 = [
	# misc
	'parking', 'ordering food', 'rare genetic diseases',
	'athletic events', 'crop insurance', 'insurance', 
	'hygiene', 'groceries', 'apparel', 'furniture',
	'appliances', 'packagine', 'cloud computing',
	'parallel processing', 'research labs', 'machine shops',
	'workforce management', 'scheduling', 'resource scheduling',
	'online shopping', 'custom apparel', 'marketplaces',
	'living spaces', 'hotels', 'real estate', 'education',
	'data analytics', 'the self-employed', 'contractors',
	'freelancers', 'engineers', 'students', 'design', 
	'circuits', 'prediction markets', 'hospitals', 'newspapers',
	'cancer detection',
	# energy
	'energy', 'solar energy', 'wind energy', 'nuclear energy', 
	'natural gas', 'hydroelectric energy', 'batteries', 
	'grid scale energy', 'energy transmission', 
	'renewable energy',	
	# AI
	'artificial intelligence', 'search', 
	'automated reasoning', 'machine learning', 
	'neural networks', 'machine translation',
	# robotics
	'robotics', 'industrial robots', 'medical robots',
	'educational robots', 'construction robots', 
	# biotech
	'biotechnology', 'agricultural technology', 
	'bioinformatics', 'genomics', 'genetic engineering',
	# healthcare
	'healthcare',
	# pharmaceuticals
	'pharmaceuticals',
	# education
	'education', 
	# human augmentation
	'human augmentation', 'reproductive technology',
	'plastic surgery', 'orthodontics', 'prosthetics',
	'medical implants', 'nootropics', 'gene therapy',
	# virtual/augmented reality
	'VR/AR',
	# transportation
	'transportation', 
	# housing
	'housing', 
	# programming tools
	'programming tools', 
	# peer-to-peer entertainment
	'peer-to-peer entertainment', 
	# enterprise software
	'enterprise software', 
	# finincial services
	'financial services', 
	# computer security
	'computer security', 
	# global health
	'global health', 
	# underserved communities
	'underserved communities', 
	# food and farming
	'food and farming', 
	# mass media
	'mass media',
	# news
	'news',
	# water
	'water purification', 'irrigation', 
	'water use effeciency', 
	'water storage', 'water transportation'
]

def get_alexa_rank(url):
    url = "http://data.alexa.com/data?cli=10&dat=s&url=" + url
    r = requests.get(url)
    soup = BS(r.content, "lxml")
    reach = soup.find('reach')
    if reach:
        rank = reach['rank']
    else:
        rank = -1
    return rank

ranks = []
for i in range(0, yclist.shape[0]):
    row = yclist.iloc[i]
    rank_i = get_alexa_rank(row['URL'])
    print('Got rank for %s' %row['Name'])
    ranks.append((row['Name'], rank_i))

ranks = [(r[0], int(r[1])) for r in ranks]
ranks = [r for r in ranks if r[1] != -1]
ranks = sorted(ranks, key = lambda x: x[1])
ranks2 = [r[1] for r in ranks]
max_rank = max(ranks2) + 1
ranks2 = [(max_rank - r) for r in ranks2]
ranks_sum = sum(ranks2)
ranks2 = [r / ranks_sum for r in ranks2]
ranks1 = [r[0] for r in ranks]
targets.extend(targets2)
def generate():
    entity = choice(ranks1, 1, p=ranks2)[0]
    print(entity, 'for', random.choice(targets))
    yc_row = yclist[yclist['Name'] == entity]
    yc_loc = yc_row.index[0]
    loc = yclist.index.get_loc(yc_loc)
    print('The description for %s on YClist.com is: %s' % \
          (entity , yclist.iloc[loc]['Description']))

generate()
