import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import random

def operation(seed_term):
    operations = [
        'Flip %s vertically, horizontally, or inside out.' %seed_term,
        'Rotate %s in physical or abstract space.' %seed_term,
        'Resize %s (What about a giant version or a tiny one?)' %seed_term,
        'Change %s from analog to digital or vice versa.' %seed_term,
        'Change %s from 3D to 2D or vice-versa.' %seed_term,
        'Change the focal point of %s (perhaps to something that was previously ignored.)' %seed_term,
        'Change %s\'s method of control. (Ex: from text to voice control.)' %seed_term,
        'change the material (Ex: from wood to steel, from Objective-C to Python.)',
        'change the colors',
        'make the product from opt in to opt out or vice-versa.',
        'change the height',
        'flexibility vs. usability',
        'form change',
        'change in control mapping',
        'fixed vs. variable',
        'symmetric vs. asymmetric',
        'conjunctive vs. disjunctive vs. compensatory',
        'reorder']
    return random.choice(operations)