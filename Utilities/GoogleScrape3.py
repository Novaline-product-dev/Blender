import os
UtilPath = os.getenv('HOME') + '/Documents/Blender/Utilities'
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(UtilPath)
import scraperfunctions


scraperfunctions.google_scrape("3D printing", 5, BlenderPath)
