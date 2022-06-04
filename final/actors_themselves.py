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
        soup.select_one('.sc-iNFqmR jiVhzd').decompose()
    except:
        a = 1
    text = soup.find_all('p')
    text_temp = ''
    for ct in range(len(text)):
        text_temp += text[ct].text
    text = text_temp
    text = text.lower()
    text = text.replace('this site is protected by recaptcha and the google privacy policy and '
                        'terms of service apply','')
    text = text.replace('”sign up for exclusive newsletters, comment on stories, '
                        'enter competitions and attend events', '')
    text = text.replace('by clicking sign up you confirm that '
                        'your data has been entered correctly and you have read and agree to our '
                        'terms of use, cookie policy and privacy notice','')
    file.close()

    return text

def tokens(text):
    import string
    import nltk
    from nltk.corpus import stopwords
    #nltk.download('stopwords')
    english_stopwords = stopwords.words("english")
    text_nostopwords = ''
    text = text.split()
    for word in text:
        if word not in english_stopwords:
            text_nostopwords = text_nostopwords + word + ' '

    punctuation = string.punctuation + "&#163;@£'‘’ " + string.digits
    for symb in punctuation:
        if symb in text_nostopwords:
            text_nostopwords = text_nostopwords.replace(symb, '')
    from nltk import word_tokenize
    #nltk.download('punkt')
    text_tokens = word_tokenize(text_nostopwords)
    text_final = ''
    for token in text_tokens:
        text_final = text_final + token + ' '
    return text_final

import os
import json

name = 'smith'
magazines = ['dailymail','glamour','hellomagazine','sky','standard']
default_path = os.getcwd()
dict_magazines = {"dailymail": '',
                  "glamour": '',
                  "hellomagazine": '',
                  "sky": '',
                  "standard": ''
                  }

for magazine in magazines:
    user_path = default_path + '\\' + name + '\\' + magazine
    filelist = []
    for root, dirs, files in os.walk(user_path):
        for file in files:
            filelist.append(os.path.join(root, file))
        user_path = os.getcwd() + '\\' + name

    text_all = ''
    for article in filelist:
        if 'dailymail' in article:
            text = cleaned_article_dailymail(article)
        if 'sky' in article:
            try:
                text = cleaned_article_newsky_glamour(article)
            except:
                print(article, 'Не вошла в корпус')
        if 'glamour' in article:
            try:
                text = cleaned_article_newsky_glamour(article)
            except:
                print(article, 'Не вошла в корпус')
        if 'hello' in article:
            text = cleaned_article_hello_standard(article)
        if 'standard' in article:
            text = cleaned_article_hello_standard(article)
        text = tokens(text)
        if text.count(name) > 2:
            dict_magazines[magazine] += text


import json

with open(f"{name}_notokens_magazines.json", "w",encoding='utf-8') as write_file:
    json.dump(dict_magazines, write_file)

