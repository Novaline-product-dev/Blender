import requests, time
import numpy as np
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

def get_tickers(ind):
    ticker_url = 'http://finviz.com/screener.ashx?v=161&f=ind_' + \
        ind + '&ft=2'
    r = requests.get(ticker_url)
    soup = BS(r.text, 'lxml')
    td = soup('td', class_="screener-body-table-nw")
    tickers = []
    for tag in td:
        ticker_string = tag.a['href']
        ticker_string = ticker_string.replace('quote.ashx?t=', '')
        ticker_string = ticker_string.replace('&ty=c&p=d&b=1', '')
        tickers.append(ticker_string)
    tickers = list(set(tickers))
    return tickers

def get_avg_margin(tickers):
    margins = []
    n_valid = 0
    running_total = 0
    for ticker in tickers:
        print('Getting margin for', ticker)
        time.sleep(5)
        margin_url = 'http://finviz.com/quote.ashx?t=' + ticker + \
            '&ty=c&p=d&b=1'
        r = requests.get(margin_url)
        soup = BS(r.text, 'lxml')
        td = soup('td')
        for i, tag in enumerate(td):
            try:
                if str(tag['title']).find('body=[Gross Margin (ttm)]') > 0:
                    gm_loc = i + 1
            except:
                continue
        margin = td[gm_loc].text
        if margin != '-':
            value = float(margin.replace('%', ''))
            running_total += value
            n_valid += 1
    if n_valid >= 1:
        return running_total / n_valid
    else:
        return -9999

inds = get_industries()
for i, ind in enumerate(inds):
    print('Current industry: ', ind[1])
    tickers = get_tickers(ind[0])
    print('Tickers for this industry:', tickers)
    avg_margin = get_avg_margin(tickers)
    inds[i] = (ind[0], ind[1], avg_margin)

with open("gross_margins.p", "wb") as f:
    pickle.dump(inds, f)