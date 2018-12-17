import numpy as np
import spacy


nlp = spacy.load('en')

def indef_art_format(string):
	if string[0].lower() in ['a', 'e', 'i', 'o', 'u']:
		return('an')
	else:
		return('a')

class physical_product:

    def __init__(self, name, components):
        self.components = components
        self.name = name


    def enlarge(self):
    	component_id = np.random.randint(len(self.components), size=1)
    	comp_name = self.components[component_id[0]]
    	indef_art = indef_art_format(self.name)
    	print('%s.upper() %s, but with a much bigger %s.' %(self.name, comp_name))



sb = physical_product('skateboard')