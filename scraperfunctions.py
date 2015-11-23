## Defines the functions that will be used in GoogleScrape3.py

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
            wait_time=random.random()+0.6 # So as to be inconspicuous
            time.sleep(wait_time)

    browser.quit()

    print (address_book)
