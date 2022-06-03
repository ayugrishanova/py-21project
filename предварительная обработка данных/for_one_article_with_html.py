from bs4 import BeautifulSoup
import string
import nltk

# удаление html-тэгов

file = open('test.txt', "r", encoding="utf-8")
contents = file.read()
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
#добавляем имя актора в стоп-слова
english_stopwords = stopwords.words("english")
english_stopwords.append('rowling')
english_stopwords.append('jk')
english_stopwords.append('joanna')
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

print(fdist.most_common(50))

#создание облака частотных слов с помощью matplotlib

#pip install worldcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text_raw = " ".join(text_lemma)
wordcloud = WordCloud(width=1000, height=1000, stopwords = stops_list, background_color = "#fff5ee", colormap = "tab10").generate(text_raw)
wordcloud.to_file('wordcloud.png')




