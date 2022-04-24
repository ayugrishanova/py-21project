import requests
from bs4 import BeautifulSoup as bs
import re
import time

file_out = open('rowling_magazines.txt', 'w', encoding='utf-8')
query = 'Kanye West news'
query = query.replace(' ', '+')
url = f'https://google.com/search?q={query}'
user_agent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
headers = {'user-agent': 'MOBILE_USER_AGENT'}
resp = requests.get(url, headers=headers)
time.sleep(3)
soup = bs(resp.content, 'lxml')
print(resp.status_code)
results = []
for div in soup.find_all('div'):
    for link in div.find_all('a'):
        if '/url?q=https://' in str(link):
            link_result = re.search(r'https.*?(?=&amp)', str(link)).group()
            if link_result not in results:
                if 'google.com' not in link_result:
                    results.append(link_result)
#for page in link_result:
    #print(page, file=file_out)
file_out.close()











