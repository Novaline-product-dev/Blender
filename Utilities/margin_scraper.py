import requests
from bs4 import BeautifulSoup as BS

def get_industries():
    '''Gets industry names from finviz.'''
    r = requests.get('http://finviz.com/screener.ashx')
    soup = BS(r.text, 'lxml')
    td = soup('td')
    for i, tag in enumerate(td):
        if str(tag.span).find('header=[Industry]') > 0:
            ind_loc = i + 1
    ind_td = td[ind_loc]
    html_opts = ind_td.find_all('option')
    inds = []
    finviz_inds = []
    nice_inds = []
    for opt in html_opts:
        finviz_inds.append(opt['value'])
        nice_inds.append(opt.text)
        inds.append((opt['value'], opt.text))
    to_drop = set(['', 'stocksonly', 'exchangetradedfund', 'modal'])
    inds = [el for el in inds if el[0] not in to_drop]
    return inds

inds = get_industries()

url = 'http://finviz.com/screener.ashx?v=161&f=ind_' + \
    inds[0][0] + '&ft=2'
r = requests.get(url)
soup = BS(r.text, 'lxml')
td = soup('td', class_="screener-body-table-nw")
# Next get tickers and look them up using FINVIZ HTTP syntax, scrape gross margin and place it in a list.