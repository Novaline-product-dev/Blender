#Usage Notes

This process will help you set up similarity queries on the Wikipedia corpus using `gensim`.

1. Download the [latest Wikipedia dump](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2). (This is around 14 GB.)  Create a folder with path `/Blender/aux` to store the data.  Navigate to `aux`.

2. Use Attardi's `wikiextractor` to get from the `.xml.bz2` format to HTML.  First, get the script:
 
 `git clone https://github.com/attardi/wikiextractor.git`, 
	
	then make an environment that runs Python 2.7 
	
 ```
 conda create --name python2.7 python=2.7
 source activate python2.7
 python wikiextractor/WikiExtractor.py -o wiki_html --no-templates enwiki-latest-pages-articles.xml.bz2
 ```
 This takes a _long time_.  This will make a folder called `wiki_html` and inside will be many folders, with names starting with `AA` and `AB` and so forth.  Those folders have the text of Wikipedia articles in an HTML-like format.  

3. Run `wiki_query_prep.py`, which will create a dictionary, a corpus, a model, and an index.  This will take several days, but it saves progress along the way.  In order to run this step, you must have a directory named `aux` inside `Blender`.  For Python 3.3 and above the current way to run `wiki_query_prep.py` is to import it as a module.  For example, if your terminal is in `Blender`, then use this at the command line:

	`python -m utils.wiki_sim.wiki_query_prep.py`

4. Now the module `wiki_query.py` has what it needs to work.
