import requests
from bs4 import BeautifulSoup as bs
import re
import time
import wget

file_out = open('out.txt', 'w', encoding='utf-8')
root_url = 'https://www.hellomagazine.com/tags/kanye-west/'
root = 'https://www.hellomagazine.com/'
resp = requests.get(root_url)
page = bs(resp.content, 'lxml')
time.sleep(3)
page_results = []
for div in page.find_all('div'):
    for link in div.find_all('a'):
        if 'kanye' in str(link).lower():
            link_result = re.search(r'(?<=href=").*?(?=")', str(link)).group()
            #print(link_result,file=file_out)
            if link_result not in page_results:
                if 'tags' not in link_result:
                    page_results.append(link_result)
#for page in page_results:
    #print(page,file=file_out)
path = 'C:\\Users\\Ann\\PycharmProjects\\py@21project\\' + re.findall(r'[A-z\.]+', root)[1]
#print(page_results[0])
#wget.download(page_results[0], path + f'\\{0}.html')
for i in range(len(page_results)):
    wget.download(page_results[i], path + f'\\{i}.html')
    print(i)


file_out.close()
