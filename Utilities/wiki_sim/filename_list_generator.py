## Writes the names of Wikipedia files into one text file
## (Blender/Wikipedia Network/filenames.txt),
## to be used by HTML_2_Corpus.py

import os

# Provide the path to the master directory, containing all the HTML format articles.
# This is the one that contains AA, AB, AC, AD and so on
path = os.getenv('HOME') + '/Documents/Blender/Aux/wiki_html'

# Move to the master directory
os.chdir(path)

# Obtain a list of sub-directories: AA, AB, AC and so forth
directory_list = os.listdir()

# Obtain a list of text files
filenames = []
for directory in directory_list:
    for file in os.listdir(directory):
        filenames.append(directory + '/' + file)

# Write the list of files to a text file
path = os.getenv('HOME') + '/Documents/Blender/Aux/wiki_model'
if not os.path.isdir(path):
    os.makedirs(path)
os.chdir(path)

with open('filenames.txt', 'w') as f:
    for filename in filenames:
        f.write(filename + '\n')

