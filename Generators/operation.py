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
        'Change the method of control for %s.' %seed_term,
        'Change the material or building blocks of %s.' %seed_term,
        'Change the colors, opacity, or brightness of %s.' %seed_term,
        'Change %s from opt in to opt out or vice-versa.' %seed_term,
        'Make %s much taller or much shorter' %seed_term,
        'Sacrifice features of %s for improved usability or add features to %s for improved power.' %(seed_term, seed_term),
        'Change the delivery format of %s.' %seed_term,
        'Change %s from symmetric to asymmetric or vice-versa.' %seed_term,
        'Change %s from all-or-nothing to anything counts or vice-versa.' %seed_term,
        'Change the order in which users interact with %s' %seed_term,
        'Allow consumers to spread purchase costs of %s across time or crowds.' %seed_term,
        'Make %s more portable.' %seed_term,
        'Build a platform where users can create their own %s' %seed_term,
        'Change the source of revenue from %s.' %seed_term,
        'Make %s more social.' %seed_term,
        'Allow consumers to communicate with %s or about %s' %(seed_term, seed_term),
        'Provide customized business services for the %s industry' %seed_term,
        'Decrease the production time or increase the production quality of %s.' %seed_term,
        'Change %s from disposable to durable or vice-versa.' %seed_term,
        'Make %s easier to maintain.' %seed_term,
        'Make %s more exclusive or more accessible.' %seed_term,
        'Change the target audience of %s to one that seeks a different benefit from using %s' %(seed_term, seed_term),
        'Remove an attribute from %s' %seed_term]
    return random.choice(operations)