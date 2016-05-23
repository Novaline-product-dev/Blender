import os, pickle
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Utilities')
import textFunctions
os.chdir(BlenderPath + '/Evaluators')
import ksFunctions
import text

idea3 = text.text
idea = """a machine that prints using liquid plastic bricks laser sintering machine welding fabrication"""

idea2 = """a machine that prints using liquid plastic bricks laser sintering machine welding fabrication in vs out"""
# Here I'm assuming there is some scraped text in the directory above...
textList = pickle.load( open("../fulltext.p", "rb"))
textList = [textFunctions.prune(doc) for doc in textList]

ksEvaluator = ksFunctions.ksFunctionGenerator(textList)

print(ksEvaluator(idea))
print(ksEvaluator(idea2))
print(ksEvaluator(idea3))

idea4 = idea3.replace('in', 'out')
print(ksEvaluator(idea4))