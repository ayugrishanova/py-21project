import urllib
import requests
from bs4 import BeautifulSoup

url="https://news.sky.com/topic/jk-rowling-6745"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
results = []
for a in soup.find_all('h3', class_='sdc-site-tile__headline'):
    link=a.find('a').get('href')
    final_link='https://news.sky.com'+link
    item = {
            "link": final_link
        }
    results.append(item)

for n in range(len(results)):
    file_data=requests.get(results[n]['link'])
    oh=file_data.text
    with open(f'{n}.txt','w') as f:
        f.write(oh)


