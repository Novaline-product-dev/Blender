import os
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath)
import scraperfunctions


scraperfunctions.google_scrape("3D printing", 5, BlenderPath)
