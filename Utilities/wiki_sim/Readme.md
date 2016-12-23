#Usage Notes

1. Download the [latest Wikipedia dump](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2). (This is around 14 GB.)

2. Use Attardi's `wikiextractor` to get from the .xml.bz2 format to HTML.  First, get the script:
 
 `git clone https://github.com/attardi/wikiextractor.git`, 
	
	then make an environment that runs python 2.7 
	
 ```
 conda create --name python2.7 python=2.7
 source activate python2.7
 python wikiextractor/WikiExtractor.py -o wiki_html --no-templates enwiki-latest-pages-articles.xml.bz2
 ```
 This takes a _long time_.  This will make a folder called `wiki_html` and inside will be many folders starting with `AA` and `AB` and so forth that have Wikipedia articles in an HTML-like format.  
 
3. Use `filename_list_generator.py`

4. Run `HTML_2_Corpus.py`, which will create a dictionary, a corpus, and an LSI model.  This will take days.

5. Run `wiki_script.py`, but change the target term.  Right now, the creation of the index is in `wiki_script.py`, which takes a while to run.  Several hours. Once the index is created, comment out the index code block and you can run queries.  (This is a terrible approach, obviously, and it will change very soon.  High priority.)
 

