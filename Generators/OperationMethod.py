import pickle, os, string, random, statistics
BlenderPath = os.getenv('HOME') + '/Documents/Blender'
AuxPath = os.getenv('HOME') + '/Documents/Blender/Aux'
os.chdir(BlenderPath + '/Generators')

transformationList = [
    'flip',
    'rotation',
    'resize',
    'in vs. out',
    'analog vs. digital',
    '3D vs. 2D',
    'push vs. pull',
    'reemphasize' ,
    'reparameterize',
    'change of material',
    'change of colors',
    'change the aesthetics',
    'opt in vs. opt out',
    'change the height',
    'flexibility vs. usability',
    'form change',
    'change in control mapping',
    'fixed vs. variable',
    'symmetric vs. asymmetric',
    'conjunctive vs. disjunctive vs. compensatory',
    'reorder']

