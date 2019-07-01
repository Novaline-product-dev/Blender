import os, wikipedia, spacy
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import spacy
os.chdir(os.getenv('HOME') + '/Desktop')



nlp = spacy.load('en_core_web_lg')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
term = 'skateboard'
print(f'Getting Wikipedia article for {term}.')
pg = wikipedia.page(term).content
pg = pg.replace('=', '')
pg = pg.replace('\n', ' ')
parsed = nlp(pg)
words = [w for w in parsed if w.lemma_ not in spacy_stopwords]
pos_drop = ['PUNCT', 'NUM', 'X', 'SYM', 'SPACE', 'PRON', 'PART']
words = [w for w in words if w.pos_ not in pos_drop]
words = [w for w in words if len(w.text) > 1]
words = [w for w in words if w.text is not '─']
if words[len(words) -1].text == 'References':
	words.pop(len(words) - 1)
seen = list()
tokens = list()
for w in words:
	if w.lemma_ in seen:
		continue
	else:
		seen.append(w.lemma_)
		tokens.append(w)


X = list()
for t in tokens:
	X.append(t.vector)

X = np.array(X)
pca = PCA(n_components=100)
pca.fit(X)
Xc = np.matmul(pca.components_, X.transpose()).transpose()

af = AffinityPropagation(preference=-30).fit(Xc)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)


print('Estimated number of clusters: %d' % n_clusters_)
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

with open('skateboard_schema.txt', 'w', encoding='utf-8') as f:
	for k in range(n_clusters_):
		class_members = labels == k
		class_tokens = [el[0] for el in zip(tokens, class_members) if el[1]]
		f.write(f'Cluster {k} with {len(class_tokens)} members: {class_tokens} \n')
