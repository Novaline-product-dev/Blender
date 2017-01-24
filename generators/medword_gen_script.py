import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from utils import text_fun
from generators import medword

print(' '.join(medword.median_words('..')))

