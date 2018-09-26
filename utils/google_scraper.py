import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils import scraper_fun
import pickle
import time


start_time = time.time() # For timing 
search_text = input("What do you seek? ") 
pages = int(input("How many pages of results would you like? "))

with open('search_text.p', 'wb') as f:
    pickle.dump(search_text, f)

scraper_fun.google_scrape(search_text, pages)

