## Processes the HTML-format file of all Wikipedia articles

from gensim import corpora, models, utils
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
from lxml import html

stemmer = SnowballStemmer('english')

def rmPunct(dirtyStr):
	splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
	cleanStr = ''.join(splitCleanStr)
	return(cleanStr)

def prune(doc):
    """This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    """
    # Tokenize the document and make it lowercase
    temp = utils.simple_preprocess(doc.lower())

    # Remove freestanding punctuation and punctuation in words
    temp = [w for w in temp if w not in string.punctuation]
    temp = [tf.rmPunct(w) for w in temp]

    # Remove specific tokens
    temp = [w for w in temp if w not in set(['[', ']', "'", '\n', 'com'])]

    # Remove stopwords
    temp = [w for w in temp if w not in stopwords.words('english')]

    # Stem the remaining words
    temp = [stemmer.stem(w) for w in temp]

    return temp

def textractor(file):
    """Accesses the text of files in a document (returns a list)."""
    raw_text = []
    with open(file) as f:
        soup = html.fromstring(f.read())
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def titlextractor(file):
    """Accesses the title of documents in a file (returns a list)."""
    titles=[]
    with open(file) as f:
        soup = html.fromstring(f.read())
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

# Provide a route by which to access all the files (it's just one right now)
files = ['Example_wiki_html_short.txt']

# Run through each file at a time, collecting stats about tokens
# Weird list comprehension: http://stackoverflow.com/ ...
# questions/1198777/double-iteration-in-list-comprehension
# Try reading it from bottom to top
dictionary = corpora.Dictionary(
    prune(doc)
        for file in files
            for doc in textractor(file))
# Remove words that appear only once, then remove holes
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteitems()
            if docfreq == 1]
dictionary.filter_tokens(once_ids)
dictionary.compactify()        

# Create a corpus using the previous dictionary and all the files
class MyCorpus(object):
    def __iter__(self):
        for file in files:                 # Access each file one at a time
            titles = titlextractor(file)
            docs = textractor(file)
            for title, doc in zip(titles, docs):
                yield [title, dictionary.doc2bow(prune(doc))]


corpus = MyCorpus()
for vector in corpus:
    print(vector)
    
    
