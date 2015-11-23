## Scrapes the text from the first n pages on a Google search.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import random
import requests
import pickle

start_time=time.time() # For timing the whole operation

search_text=input("What do you seek? ") # Gives us our goal
pages=int(input("How many pages of results would you like? "))

browser= webdriver.Firefox() # Establishes which web browser we will be using
browser.implicitly_wait(10)

url = 'http://www.google.com' # Target url

# Navigate to the target url
browser.get(url)
#browser.set_window_size(500,500)

# Find the text input in order to search
search_bar_id="lst-ib"

# Complete a search
elem=browser.find_element_by_id(search_bar_id)
elem.clear()
elem.send_keys(search_text, Keys.ENTER) # From the beginning input

# Obtain a list of the urls that are listed
address_book=[] #initialize list
wait = WebDriverWait(browser,10) # for allowing the page to load each time you get a new page of results

# Do this for the first (n) pages
for n in range(pages):

    # Find the 'next page' button and wait until everything is loaded
    #elem=wait.until(expected_conditions.element_to_be_clickable((By.XPATH,'//a[@id="pnnext"]')))
    
    elems = browser.find_elements_by_xpath("//ol//div//div/div/h3/a")
    for el in elems:
        url=str(el.get_attribute('href'))
        address_book.append(url)
        
    elem=browser.find_element_by_xpath('//a[@id="pnnext"]')
    if n < (pages - 1):
        elem.click()
        wait_time=random.random()+0.6 # So as to be inconspicuous
        time.sleep(wait_time)

browser.quit()

print (address_book)

# Compile the text from all the web pages
fulltext= [] # initialize empty list

for x in range(len(address_book)):
    # Retrieve the html
    r=requests.get(address_book[x])
    html=r.text

    # Remove style elements
    soup=BeautifulSoup(html,"lxml")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text() # get text

    # perhaps not entirely necessary:

    # break into lines and remove leading and trailing spaces
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
##    text=text.encode('utf-8')
    text = text.replace(',', '')

    fulltext.append(text) # append element with text from page x

for i, string in enumerate(fulltext):
    fulltext[i] = ''.join([j if ord(j) < 128 else '' for j in string])

with open("output.p", "wb") as f:
    pickle.dump(fulltext, f)

print ('Text from %s web pages scanned.' % len(address_book))
t=time.time()-start_time
print ('----- %s seconds -----' % t)
