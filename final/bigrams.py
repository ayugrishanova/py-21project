def cleaned_article_newsky_glamour(filename):
    from bs4 import BeautifulSoup
    import re
    import json

    file = open(filename, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    soup = BeautifulSoup(contents, 'lxml')
    text = soup.find("script", type="application/ld+json").text
    text = re.search(r'{.*}', text).group()
    text = json.loads(text)['articleBody']
    text = text.lower()
    file.close()

    return text

def cleaned_article_dailymail(filename):
    from bs4 import BeautifulSoup

    file = open(filename, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    soup = BeautifulSoup(contents, 'lxml')
    text = soup.find_all('p',{"class": "mol-para-with-font"})
    text_temp = ''
    for ct in range(len(text)):
        text_temp += text[ct].text
    text = text_temp
    text = text.lower()
    file.close()

    return text

def cleaned_article_hello_standard(filename):
    from bs4 import BeautifulSoup

    file = open(filename, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    soup = BeautifulSoup(contents, 'lxml')
    try:
        soup.select_one('.legal').decompose()
    except:
        a = 1
    try:
        soup.select_one('.titular-section').decompose()
    except:
        a = 1
    try:
        soup.select_one('.sc-iNFqmR').decompose()
    except:
        a = 1

    text = soup.find_all('p')
    text_temp = ''
    for ct in range(len(text)):
        text_temp += text[ct].text
    text = text_temp
    text = text.lower()
    file.close()

    return text

import nltk
from nltk import ngrams
from wordcloud import WordCloud
from collections import Counter
import json
def get_frequency(string):
    return freqbig[tuple(string.split(" "))]

dict_magazines = {"dailymail": '',
                  "glamour": '',
                  "hellomagazine": '',
                  "sky": '',
                  "standard": ''
                  }
name = 'smith'
file = open(f'{name}_notokens_magazines.json',encoding='utf-8')
data = json.load(file)
words = []
for key in data.keys():
    text = data[key].split('.')
    for sentence in text:
        bi_grams = list(ngrams(sentence.split(), 2))
        for gram in bi_grams:
            word = gram[0] + '_' + gram[1]
            words.append(word)
    for word in words:
        dict_magazines[key] += word + ' '



import json
with open(f"{name}_bigrams.json", "w",encoding='utf-8') as write_file:
    json.dump(dict_magazines, write_file)
