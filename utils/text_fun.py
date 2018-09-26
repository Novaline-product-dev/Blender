import os, string
import spacy
from lxml import html
from utils import stoplists


nlp_prune = spacy.load('en')
nlp = spacy.load('en')
#default_stop_list = set(['[', ']', '\'', '\n', '==', \
#                         'com', '\n\n', '\'s', ' ', '  ',
#                         '===', '\n\n\n'])
default_stop_list = stoplists.long_stoplist
def prune(doc, stoplist=default_stop_list, english_dict=True, ok_tags=None):
    '''This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    '''
    temp = nlp_prune(doc)
    temp = [w for w in temp if w.pos_ != 'PUNCT']
    temp = [w for w in temp if w.pos_ != 'NUM']
    if ok_tags:
        temp = [w for w in temp if w.tag_ in ok_tags]
    temp = [w for w in temp if not w.is_stop]
    if english_dict:
        temp = [w for w in temp if str(w) in nlp.vocab]
    out = [w.lemma_ for w in temp]
    out = [w for w in out if w != '-PRON-']
    out = [w for w in out if w not in stoplist]
    out = [w.strip() for w in out if w.strip()]
    out = [w for w in out if w != len(w) * w[0]]
    return out

def prune_post_parse(doc, stoplist=None, english_dict=False):
    '''This takes a single document and tokenizes the words, removes
    undesirable elements, and prepares it to be loaded into a dictionary.
    The only difference between this and prune is that it expects a parsed
    spacy document.
    '''
    if not stoplist:
        stoplist = default_stop_list
    temp = [w for w in doc if w.pos_ != 'PUNCT']
    temp = [w for w in doc if w.pos_ != 'NUM']
    temp = [w for w in temp if w.text not in stoplist]
    temp = [w for w in temp if not w.is_stop]
    if english_dict:
        temp = [w for w in temp if str(w) in nlp.vocab]
    out = [w.lemma_ for w in temp]
    return out

def prune_w2v(doc):
    stoplist = default_stop_list
    temp = [w for w in doc if w.pos_ != 'PUNCT']
    temp = [w for w in temp if w.pos_ != 'NUM']
    temp = [w for w in temp if w.text not in stoplist]
    temp = [w for w in temp if not w.is_stop]
    temp = [w for w in temp if str(w) in nlp.vocab]
    out = [w.lemma_ for w in temp]
    return out

def prune_sem(doc):
    stoplist = default_stop_list
    out = []
    for w in doc:
        temp = [w.head]
        temp.extend(list(w.children))
        if w.dep_ == 'pobj':
            temp.extend([w.head.head])
        temp = [w for w in temp if w.pos_ != 'PUNCT']
        temp = [w for w in temp if w.pos_ != 'NUM']
        temp = [w for w in temp if w.text not in stoplist]
        temp = [w for w in temp if not w.is_stop]
        temp = [w for w in temp if str(w) in nlp.vocab]
        temp = [w.text for w in temp]
        if len(temp) > 1:
            out.append(temp)
    return out

def w2v_sent_prep(article):
    spacy_art = nlp(article)
    spacy_sentences = spacy_art.sents
    sentences = [prune_post_parse(sent) for sent in spacy_sentences]
    sentences = [el for el in sentences if el]
    return sentences

def text_extractor(file_name):
    '''Gets body text from html docs produced by wikiextractor.'''
    raw_text = []
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for doc in soup.xpath('//doc'):
            raw_text.append(doc.text)
    return raw_text

def title_extractor(file_name):
    '''Gets titles from html docs produced by wikiextractor.'''
    titles=[]
    with open(file_name, 'rb') as f:
        soup = html.fromstring(f.read().decode('utf8', 'ignore'))
        for title in soup.xpath('//@title'):
            titles.append(title)
    return titles

def line_streamer(path, N=None):
    '''Generator function for building the dictionary.'''
    i = 0
    with open(path, 'rb') as f:
        for line in f:
            if N:
                i += 1
                if i%10000:
                    pct_complete = round(i / N * 100, 2)
                    print('\r %d%% finished' %pct_complete, 
                        end="", flush=True) 
            yield line.decode('utf8', 'ignore').split() 

def prep_save(input_path, titles_path, articles_path):
    if os.path.isfile(titles_path) and os.path.isfile(articles_path):
        print('Prepped files already on disk at', titles_path,
            ' and ', articles_path)
    else:
        articles = text_extractor(input_path)
        titles = title_extractor(input_path)
        titles_out = []
        articles_out = []
        for title, article in zip(titles, articles):
            prepped_title = ''.join((title, '\n'))
            article_tokens = prune(article)
            if len(article_tokens) >= 5:
                titles_out.append(prepped_title)
                tokens_string = ' '.join(article_tokens)
                prepped_art = ''.join((tokens_string, '\n'))
                articles_out.append(prepped_art)
        assert len(articles_out) == len(titles_out)
        with open(titles_path, 'wb') as f:
            for title in titles_out:
                f.write(title.encode('utf8'))
        with open(articles_path, 'wb') as f:
            for article in articles_out:
                f.write(article.encode('utf8'))

def prep_save_w2v(input_path, sentences_path):
    if os.path.isfile(sentences_path):
        print('Prepped files already on disk at', sentences_path)
    else:
        articles = text_extractor(input_path)
        sentences_out = []
        for article in articles:
            sents = nlp(article).sents
            for sent in sents:
                prepped_sent = prune_w2v(sent)
                if len(prepped_sent) > 2:
                    sentences_out.append(prepped_sent)
        with open(sentences_path, 'wb') as f:
            for sentence in sentences_out:
                to_write = ' '.join(sentence)
                to_write = ' '.join(to_write.split())
                to_write = ''.join((to_write, '\n'))
                f.write(to_write.encode('utf8'))


def transform_texts(texts):
    for doc in nlp.pipe(texts, n_threads=4):
        # Iterate over base NPs, e.g. "all their good ideas"
        for np in doc.noun_chunks:
            # Only keep adjectives and nouns, e.g. "good ideas"
            while len(np) > 1 and np[0].dep_ not in ('amod', 'compound'):
                np = np[1:]
            if len(np) > 1:
                # Merge the tokens, e.g. good_ideas
                np.merge(np.root.tag_, np.text, np.root.ent_type_)
            # Iterate over named entities
            for ent in doc.ents:
                if len(ent) > 1:
                    # Merge them into single tokens
                    ent.merge(ent.root.tag_, ent.text, ent.label_)
        token_strings = []
        for token in tokens:
            text = token.text.replace(' ', '_')
            tag = token.ent_type_ or token.pos_
            token_strings.append('%s|%s' % (text, tag))
        yield ' '.join(token_strings)


def prep_save_sem(input_path, sentences_path):
    if os.path.isfile(sentences_path):
        print('Prepped files already on disk at', sentences_path)
    else:
        articles = text_extractor(input_path)
        sentences_out = []
        for article in articles:
            sents = nlp(article).sents
            for sent in sents:
                prepped_sents = prune_sem(sent)
                for prepped_sent in prepped_sents:
                    sentences_out.append(prepped_sent)
        with open(sentences_path, 'wb') as f:
            to_write_old = ''
            for sentence in sentences_out:
                to_write = ' '.join(sentence)
                to_write = ' '.join(to_write.split())
                to_write = ''.join((to_write, '\n'))
                if to_write == to_write_old:
                    continue
                to_write_old = to_write
                f.write(to_write.encode('utf8'))


class WikiCorpus(object):
    def __init__(self, articles_path, gensim_dictionary, N=None):
        self.dictionary = gensim_dictionary
        self.articles_path = articles_path
        if N:
            self.N = N

    def __iter__(self):
        with open(self.articles_path, 'r') as f:
            i = 0
            for line in f:
                i += 1
                if self.N:
                    if i%10000:
                        pct_complete = round(i / self.N * 100, 2)
                        print('\r %d%% finished' %pct_complete, 
                            end="", flush=True) 
                tokens = line.split()
                yield self.dictionary.doc2bow(tokens)
