from bs4 import BeautifulSoup as BS
import requests

term = 'ballpoint pen'
urls = gather_urls(term, 1)
dollar_count = 0
for url in urls:
    r = requests.get(url)
    soup = BS(r.content, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()
    plainish = soup.get_text()
    page_dollar_count = plainish.count('$')
    print(page_dollar_count)
    dollar_count += page_dollar_count
print('Total: ', dollar_count)