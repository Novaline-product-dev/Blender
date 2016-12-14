#Usage Notes

1. Download the [latest Wikipedia dump](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2).

2. Use Attardi's wikiextractor to get from the .xml.bz2 format to HTML.  First, get it:
 
 `git clone https://github.com/attardi/wikiextractor.git`, 
	
	then make an environment that runs python 2.7 
	
 ```
 conda create --name python2.7 python=2.7
 source activate python2.7
 python wikiextractor/WikiExtractor.py -o wiki_html --no-templates enwiki-latest-pages-articles.xml.bz2
 ```
 This takes a _long time_.  This will make a folder called `wiki_html` and inside will be many folders starting with `AA` and `AB` and so forth that have Wikipedia articles in an HTML-like format.  
 
3. Use `filename_list_generator.py`

4. Clean the text > Form a dictionary > Change each article to BOW > Convert from BOW to TF-IDF > Convert from TF-IDF to LSI > Peform similarity analysis

Blender/Wikipedia Newtork/wikiScript.py gives a nice summary.  So doeas HTML_2_Corpus.py at the end.
