import os
UtilPath = os.getenv('HOME') + '/Documents/Blender/Utilities'
os.chdir(UtilPath)
import scraperfunctions
import pickle
import time

BlenderPath = os.getenv('HOME') + '/Documents/Blender'

start_time = time.time() # For timing 
search_text = input("What do you seek? ") 
pages = int(input("How many pages of results would you like? "))

with open(BlenderPath + "/search_text.p", "wb") as f:
    pickle.dump(search_text, f)

scraperfunctions.google_scrape(search_text, pages, True)

