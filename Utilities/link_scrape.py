import requests
from bs4 import BeautifulSoup as BS
import re

search_term = 'work light'
page_count = 1

stop_str1 = 'Shop for ' + search_term + ' on Google'
stop_str2 = 'Images for ' + search_term
stop_list = [stop_str1, stop_str2]

address_book = []
for i in range(1, page_count + 1):
    start = (i - 1) * 10
    if start == 0:
        r = requests.get('http://www.google.com/search?q=' + search_term)
    else:
        r = requests.get('http://www.google.com/search?q=' + search_term + '&start=' + str(start))
    soup = BS(r.text, 'lxml')
    blue_links = soup('h3', class_ = 'r')
    for link in blue_links:
        if link.text not in stop_list:
            href = link.a['href']
            url = href.replace('/url?q=', '')
            url = re.sub('&sa=.*', '', url)
            if not re.search('/search\\?q=', url):
                address_book.append(url)
    print('Page ' + str(i) + ' of Google urls gathered.')

print('\n'.join(address_book))