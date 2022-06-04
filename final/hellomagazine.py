import urllib
import requests
from bs4 import BeautifulSoup

url="https://www.hellomagazine.com/tags/jk-rowling/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
results = []
for a in soup.find_all('article', class_='module headline'):
    link=a.find('a').get('href')
    item = {
            "link": link
        }
    results.append(item)

for n in range(len(results)):
    file_data=requests.get(results[n]['link'])
    oh=file_data.text
    with open(f'{n}.txt','w') as f:
        f.write(oh)


