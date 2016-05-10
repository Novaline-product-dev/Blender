## Defines the functions that will be used in GoogleScrape3.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
import time
import random
import pickle

def gather_urls(search_term, page_count): # Gathers page_count urls from Google

    browser= webdriver.Firefox() # Establishes which web browser we will be using
    browser.implicitly_wait(10)

    url = 'http://www.google.com' # Target url

    # Navigate to the target url
    browser.get(url)

    # Find the text input in order to search
    search_bar_id="lst-ib"

    # Complete a search
    elem=browser.find_element_by_id(search_bar_id)
    elem.clear()
    elem.send_keys(search_term, Keys.ENTER) # From the beginning input

    # Obtain a list of the urls that are listed
    address_book=[] #initialize list
    wait = WebDriverWait(browser,10) # for allowing the page to load each time you get a new page of results

    # Do this for the first (n) pages
    for n in range(page_count):

        # Find the 'next page' button and wait until everything is loaded
        #elem=wait.until(expected_conditions.element_to_be_clickable((By.XPATH,'//a[@id="pnnext"]')))
        
        elems = browser.find_elements_by_xpath("//ol//div//div/div/h3/a")
        for el in elems:
            url=str(el.get_attribute('href'))
            address_book.append(url)
            
        elem=browser.find_element_by_xpath('//a[@id="pnnext"]')
        if n < (page_count - 1):
            elem.click()
            wait_time=random.random() + 0.6 # So as to be inconspicuous
            time.sleep(wait_time)

    browser.quit()

    return (address_book)

def text_clean(text): # Alters the text to a desireable format
    # The following was found at http://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
    # perhaps not entirely necessary:

    # break into lines and remove leading and trailing spaces
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    ##    text=text.encode('utf-8') # only if in python 2

    # Other modifications
    text = text.replace(',', '')

def retrieve_text(address_book):  # Scrapes the text from a list of urls
    fulltext = [] # initialize empty list
    global trouble_child
    trouble_child = [] # initialize list to find pages that don't work

    for x in range(len(address_book)):
        # Retrieve the html
        proceed = "y"
        try:
            r = requests.get(address_book[x])
            html = r.text
        except:
            trouble = address_book[x]
            trouble_child.append(trouble)
            proceed = "n"
            pass

        if proceed == "y":
            # Remove style elements
            soup = BeautifulSoup(html, "lxml")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text() # get text

            text_clean(text) # Puts the text in a useful format

            fulltext.append(text) # append element with text from page x

            # To track progress:
            print ("Page: %s, %s to go" %(x + 1, len(address_book) - x - 1))

    for i, string in enumerate(fulltext):
        fulltext[i] = ''.join([j if ord(j) < 128 else '' for j in string])

    with open("fulltext.p", "wb") as f:
        pickle.dump(fulltext, f)

    return trouble_child
