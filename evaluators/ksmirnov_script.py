import os, pickle
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
os.chdir(BlenderPath + '/Utilities')
import text_fun
os.chdir(BlenderPath + '/Evaluators')
import ksmirnov_fun

idea = """a machine that prints using liquid plastic bricks laser sintering machine welding fabrication"""

# Here I'm assuming there is some scraped text in the directory above...
textList = pickle.load( open("../fulltext.p", "rb"))
textList = [text_fun.prune(doc) for doc in textList]

ksEvaluator = ksmirnov_fun.ksFunctionGenerator(textList)

print(ksEvaluator(idea))
