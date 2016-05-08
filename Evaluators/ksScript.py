import os, pickle
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Evaluators')
import ksFunctions
import textFunctions

idea = """a machine that prints using liquid plastic bricks laser sintering machine welding fabrication"""

# Here I'm assuming there is some scraped text in the directory above...
textList = pickle.load( open("../fulltext.p", "rb"))
textList = [textFunctions.prune(doc) for doc in textList]

ksEvaluator = ksFunctions.ksFunctionGenerator(textList)

print(ksEvaluator(idea))