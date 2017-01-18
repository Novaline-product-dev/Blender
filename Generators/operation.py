import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
import random
from nltk.corpus import wordnet as wn


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
    processes = ['design', 'purchase', 'maintenance', 'core function', 'auxilliary functions']
    return random.choice(processes)
    
def business_model():
    b_mods = ['Allow customers to name a price (ex: Priceline)',
    'Use offer aggregation (ex: Kayak, eBay, Amazon)',
    'Change to just-in-time production, or the pull method (ex: Dell, Toyota)',
    'Growth first, profit later (ex: Amazon, many startups)',
    'The modern franchise (ex: Macdonalds)',
    'Software first, hardware to follow (ex: Microsoft, Google, Amazon)',
    'Walled-garden product line (ex: Apple, Google)',
    'The P2P Revolution (ex: Etsy, Kickstarter, Paypal, Craigslist',
    'Vertical integration (ex: Tesla)',
    'Advertiser model: if you drive traffic, sell it (ex: Google, FB)', 
    'Data model: gather info and sell access (ex: Bloomberg)',
    'Merchant model: resell (ex: TJMaxx)',
    'Brokerage model: sell knowledge about an activity/service (ex: Goldman Sachs)',
    'Affiliate/commision model: take a cut of sales you create (ex: Kickstarter)',
    'Auction model: gather buyers and sellers in your industry (ex: eBay, Amazon)',
    'Add-on Model: razor and blades or upgrades (ex: Gillette, Super Mario Run)',
    'Direct Sales, no middle retailer (ex: Warby-Parker)',
    'Freemium or try-before-you-buy (ex: AWS Free Tier)',
    'Low-cost + upsell (ex: Ryanair)',
    'Pay-as-you-go (ex: Utilities, AWS)',
    'All You Can Use/Eat (ex: Noun Project Pro)',
    'Crowdsource a new launch (ex: Pebble)',
    'Price by algorithm (ex: Uber, Logo Pizza, Jet)']
    return random.choice(b_mods)

def opposites():
    alts = [
        ['bumpy/rough', 'smooth'],
        ['analog', 'digital'],
        ['3D', '2D'],
        ['opaque', 'transparent'],
        ['opt-in', 'opt-out'],
        ['symmatric', 'assymetric'],
        ['temporary', 'durable']
    ]
    return random.choice(random.choice(alts))

def operation(seed_term):
    operations = [
        'Flip the %ss vertically, horizontally, or inside out.' %seed_term,
        'Rotate the %s in physical or abstract space.' %seed_term,
        'Resize the %s (A giant version? A tiny one?)' %seed_term,
        'Change distribution of %ss from inventory to made-to-order or vice-versa.' %seed_term,
        'Change the %s from analog to digital or vice versa.' %seed_term,
        'Change the focal point of %ss (perhaps to something that was previously ignored.)' %seed_term,
        'Change the method of control for the %s.' %seed_term,
        'Change the material or building blocks of the %s.' %seed_term,
        'Change the colors, opacity, or brightness of the %s.' %seed_term,
        'Make %s much taller or much shorter' %seed_term,
        'Sacrifice features of %s for improved usability or add features to %s for improved power.' %(seed_term, seed_term),
        'Change the delivery format of %s.' %seed_term,
        'Change the order in which users interact with %s' %seed_term,
        'Allow consumers to spread purchase costs of %s across time or crowds.' %seed_term,
        'Make %s more portable.' %seed_term,
        'Build a platform where users can create their own %s' %seed_term,
        'Change the source of revenue from %s.' %seed_term,
        'Make %s more social.' %seed_term,
        'Allow consumers to communicate with %s or about %s' %(seed_term, seed_term),
        'Provide customized business services for the %s industry.' %seed_term,
        'Decrease the production time or increase the production quality of %s.' %seed_term,
        'Make %s easier to maintain.' %seed_term,
        'Make %s more exclusive or more accessible.' %seed_term,
        'Change the target audience of %s to one that seeks a different benefit.' %seed_term,
        'Remove an attribute from %s' %seed_term,
        'Automate the %s of %s' %(process(), seed_term),
        'For %s, experiment with this business model: %s' %(seed_term, business_model())
        ]
    return random.choice(operations)
