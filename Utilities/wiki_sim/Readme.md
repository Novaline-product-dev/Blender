#Usage Notes

This process will help you set up similarity queries on the Wikipedia corpus using `gensim`.

1. Download the [latest Wikipedia dump](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2). (This is around 14 GB.)  Create a folder with path `/Blender/Aux` to store the data.  Navigate to `Aux`.

2. Use Attardi's `wikiextractor` to get from the `.xml.bz2` format to HTML.  First, get the script:
 
 `git clone https://github.com/attardi/wikiextractor.git`, 
	
	then make an environment that runs Python 2.7 
	
 ```
 conda create --name python2.7 python=2.7
 source activate python2.7
 python wikiextractor/WikiExtractor.py -o wiki_html --no-templates enwiki-latest-pages-articles.xml.bz2
 ```
 This takes a _long time_.  This will make a folder called `wiki_html` and inside will be many folders, with names starting with `AA` and `AB` and so forth.  Those folders have the text of Wikipedia articles in an HTML-like format.  
 
3. Use `filename_list_generator.py`.  This simply runs through the folders and creates a list of the filenames so the next script can read them.

4. Run `wiki_query_prep.py`, which will create a dictionary, a corpus, a model, and an index.  This will take several days.

5. Run `wiki_query.py`, but change `query_term` to whatever you want.
 

