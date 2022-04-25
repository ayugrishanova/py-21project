import urllib
import requests
from bs4 import BeautifulSoup

url="https://www.glamourmagazine.co.uk/topic/jk-rowling"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
results = []
for a in soup.find_all('div', class_='SummaryItemContent-gYA-Dbp bHOHql summary-item__content'):
    link=a.find('a').get('href')
    final_link='https://www.glamourmagazine.co.uk'+link
    item = {
            "link": final_link
        }
    results.append(item)

for n in range(len(results)):
    file_data=requests.get(results[n]['link'])
    oh=file_data.text
    with open(f'{n}.txt','w') as f:
        f.write(oh)


