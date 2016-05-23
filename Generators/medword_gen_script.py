import os
UtilPath = os.getenv('HOME') + '/Documents/Blender/Utilities'
os.chdir(UtilPath)
import text_fun
os.chdir(os.getenv('HOME') + '/Documents/Blender/Generators')
import medword
os.chdir(os.getenv('HOME') + '/Documents/Blender')


print(' '.join(medword.median_words('..')))

# Plot.  Comment if you don't care.
#--------------------------------------------------------------------
#text_fun.textNetworkPlot(textList)
