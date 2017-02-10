import requests
import random
from bs4 import BeautifulSoup as BS 


url = 'http://www.startupranking.com/top/united-states'
r = requests.get(url)
soup = BS(r.content, 'lxml')
soup = soup.tbody
soup_names = soup.find_all(class_ = 'name')
names = []
links = []
descriptions = []
for tag in soup_names:
	url_end = tag.a['href']
	spec_page = requests.get('http://www.startupranking.com' + url_end)
	spec_soup = BS(spec_page.content, 'lxml')
	su_info = spec_soup.find_all(class_ = 'su-info')
	raw_description = su_info[0].find_all('p')[0].get_text()
	raw_description = raw_description.replace('...\nSee More\n', '')
	raw_description = raw_description.replace('\n', '')
	descriptions.append(raw_description.strip())
	name = tag.a.get_text()
	names.append(name)
	print('Finished with %s' %name)

locs = random.sample(range(0, len(names) - 1), 2)
print('Combine %s and %s' %(names[locs[0]], names[locs[1]]))
print('Description for ', names[locs[0]], ': ', descriptions[locs[0]])
print('Description for ', names[locs[1]], ': ', descriptions[locs[1]])