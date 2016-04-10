## Writes the names of Wikipedia files into one text file
## (Blender/Wikipedia Network/filenames.txt),
## to be used by HTML_2_Corpus.py

import os

# Provide the path to the master directory, containing all the HTML format articles.
# This is the one that contains AA, AB, AC, AD and so on
print('Please enter the full path of the master directory --')
print('ex: /fslhome/cbell75/wikidump/wiki_to_html2')
path = input('This is the one that contains AA, AB, AC, AD, and so on.\n')

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
os.chdir(os.environ['HOME'])
os.chdir('Documents/Blender')
os.chdir('Wikipedia Network')
with open('filenames.txt', 'w') as f:
    for filename in filenames:
        f.write(filename + '\n')
