def cleaned_article(filename):
    from bs4 import BeautifulSoup
    import string
    import nltk

# удаление html-тэгов    
    
    file = open(filename, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    soup = BeautifulSoup(contents, 'lxml')

    html_free = soup.get_text('\n', strip='True')
    text = html_free.lower()

# удаление пунктуации и прочих лишних симвлов    
    
    cleaning = string.punctuation + "\n\xa0«»\t—…" + string.digits + "'‘’"
    new_text = ''
    for ch in text:
        if ch not in cleaning:
            new_text += ch

 # токенизация           
            
    from nltk import word_tokenize
    #nltk.download('punkt')
    text_tokens = word_tokenize(new_text)
    
 # удаление стоп-слов   

    from nltk.corpus import stopwords
    #nltk.download('stopwords')
    english_stopwords = stopwords.words("english")
    no_stopwords = ''
    for w in text_tokens:
        if w not in english_stopwords:
            no_stopwords = no_stopwords + w + ' '

# лемматизация и формирование списка частотных лемм
    #pip install -U pip setuptools wheel
    #pip install -U spacy
    #python -m spacy download en_core_web_sm

    import spacy

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(no_stopwords)
    lemmatization = []
    for token in doc:
        lemmatization.append(token.lemma_)

    text_lemma = nltk.Text(lemmatization)

    from nltk.probability import FreqDist
    fdist = FreqDist(text_lemma)
    
    return no_stopwords, fdist


import os

name=str(input('Напишите имя знаменитости с маленькой буквы, например rowling: '))
user_path=str(input('Введите путь: '))
filelist = []
for root, dirs, files in os.walk(user_path): 
    for file in files: 
        filelist.append(os.path.join(root,file)) 
        
 # формирования словаря со статьями, в которых имя актора упоминается 3 и более раз       

list_articles = dict()

for n in range(len(filelist)):
    processed_article = cleaned_article(filelist[n])
    if int(processed_article[1][name]) >= 3:
        list_articles.update({ n : processed_article[0] })
        
 # создание файла json с корпусом       

import json

with open("corpus.json", "w") as write_file:
    json.dump(list_articles, write_file)
        
