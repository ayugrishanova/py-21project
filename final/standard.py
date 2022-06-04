import urllib
import requests
from bs4 import BeautifulSoup

url="https://www.standard.co.uk/topic/jk-rowling"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
results = []
for a in soup.find_all('h2', class_='sc-eoXOpV eKnhtJ sc-kMizLa huNIDp'):
    link=a.find('a').get('href')
    if 'rowling' in link:
        final_link='https://www.standard.co.uk'+link
        item = {"link": final_link }
        results.append(item)

for n in range(len(results)):
    file_data=requests.get(results[n]['link'])
    oh=file_data.text
    with open(f'{n}.txt','w') as f:
        f.write(oh)


