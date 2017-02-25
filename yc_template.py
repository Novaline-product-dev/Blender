import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils import spacy_analogy
import spacy
import requests
import pandas as pd
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
targets = []
for i, row in yclist.iterrows():
    description = row['Description']
    for_ind = description.find('for ')
    if for_ind != -1:
        end = description.find('.')
        if end == -1:
            targets.append(description[for_ind:])
        else:
            targets.append(description[for_ind:end])
category_list = ['energy', 'AI', 'robotics', 'biotech', 'healthcare',
    'pharmaceuticals', 'education', 'human augmentation', 
    'virtual/augmented reality', 'transportation', 'housing', 
    'programming tools', 'peer-to-peer entertainment', 
    'enterprise software', 'financial services', 'computer security', 
    'global health', 'underserved communities', 'food and farming', 
    'mass media', 'news', 'water']