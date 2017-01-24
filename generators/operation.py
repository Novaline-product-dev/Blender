import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import random

def audience():
    alts = [
        'men',
        'women',
        'healthcare professionals',
        'runners',
        'creatives',
        'businesspeople',
        'parents',
        'kids',
        'the disabled',
        'students',
        'the wealthy'
        'the elderly',
        'Millenials',
        'Baby Boomers',
        'people from Generation X',
        'busy people',
        'obese people'
    ]
    return random.choice(alts)

def material():
    choices = ['acrylic', 'alloy', 'aluminum', 'brass',
        'brick', 'bronze', 'carbon', 'cardboard', 'cast iron',
        'cement', 'ceramics', 'copper', 'cotton', 'diamond', 'epoxy',
        'fiber', 'fiberglass', 'glass', 'glue', 'gold', 'iron', 'leather',
        'linen', 'nylon', 'paper', 'polyester', 'rubber', 'sand', 'silica',
        'silver', 'skin', 'steel', 'stone', 'titanium', 'vinyl', 'viscose', 
        'wood', 'wool']
    return random.choice(choices)

def process():
    alts = ['design', 'purchase', 'maintenance', 'core function', 'auxilliary functions']
    return random.choice(alts)
    
def business_model(seed_term):
    b_mods = ['allowing customers to name their own price for %ss' %seed_term,
    'using offer aggregation to sell %ss (e.g. Kayak, eBay, Amazon)' %seed_term,
    'changing to just-in-time production for %ss' %seed_term,
    'building a %s franchise' %seed_term,
    'software first, hardware to follow (ex: Microsoft, Google, Amazon)',
    'walled-garden product line (ex: Apple, Google)',
    'the P2P Revolution (ex: Etsy, Kickstarter, Paypal, Craigslist',
    'vertically integrating %s production' %seed_term,
    'gather %s-related information and sell access to it' %seed_term,
    'merchant model: resell (ex: TJMaxx)',
    'sell knowledge about an activity/service (ex: Goldman Sachs)',
    'auction %ss',
    'add-on Model: razor and blades or upgrades (ex: Gillette, Super Mario Run)',
    'direct Sales, no middle retailer (ex: Warby-Parker)',
    'freemium or try-before-you-buy (ex: AWS Free Tier)',
    'low-cost + upsell (ex: Ryanair)',
    'pay-as-you-go (ex: Utilities, AWS)',
    'all You Can Use/Eat (ex: Noun Project Pro)',
    'price by algorithm (ex: Uber, Logo Pizza, Jet)']
    return random.choice(b_mods)

def adjectives(seed_term):
    adjs = [
        'more reliable',
        'more authentic',
        'more confident',
        'brighter',
        'cleaner',
        'more social',
        'more portable',
        'lighter',
        'more secure',
        'autonomous'
    ]
    return random.choice(adjs)

def opposites(seed_term):
    alts = [['bumpy/rough', 'smooth'],
        ['analog', 'digital'],
        ['3D', '2D'],
        ['opaque', 'transparent'],
        ['opt-in', 'opt-out'],
        ['symmatric', 'assymetric'],
        ['temporary', 'durable'],
        ['minimalist', 'feature-rich'],
        ['powerful', 'efficient'],
        ['exclusive', 'accessible']]
    alt = random.choice(alts)
    idea = 'Make %ss more %s or more %s.' %(seed_term, alt[0], alt[1])
    return idea

def transformation(seed_term):
    transformed = [
    'How about a %s that is horizantally reversed?' %seed_term,
    'Try a %s that is vertically flipped.' %seed_term,
    'Make a %s that is inside out.' %seed_term,
    'A giant %s!' %seed_term,
    'A tiny %s, maybe for a new purpose.' %seed_term
    ]
    return random.choice(transformed)

def platform_functions(seed_term):
    funs = [
        'Build a platform where users can create their own %s.' %seed_term,
        '''Build a platform where people communicate 
        with each other using %ss or about %ss.''' %(seed_term, seed_term),
        'Build a platform where users can buy and sell %ss.' %seed_term
    ]
    return random.choice(funs)

def control_types():
    types = [
        'with software',
        'using an algorithm',
        'with voice',
        'using touch',
        'with a stylus',
        'via a command line',
        'remotely'
    ]
    return random.choice(types)

def template(seed_term):
    templates = [
        transformation(seed_term),
        opposites(seed_term),
        'Allow users to control %ss %s.' %(seed_term, control_types()),
        'Literally or figuratively, make a %s %s.' %(material(), seed_term),
        'Make a %s that is %s.' %(seed_term, adjectives(seed_term)),
        platform_functions(seed_term),
        'Make a %s for %s.' %(seed_term, audience()),
        'Allow users to automate the %s of %ss.' %(process(), seed_term),
        'Experiment with %s.' %business_model(seed_term)
        ]
    return random.choice(templates)

for i in range(0, 10):
    print('\n', template('notebook'))
