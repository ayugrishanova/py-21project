from bs4 import BeautifulSoup
import string
import nltk

file = open('test.txt', "r", encoding="utf-8")
contents = file.read()
soup = BeautifulSoup(contents, 'lxml')

html_free = soup.get_text('\n', strip='True')

text = html_free.lower()

cleaning = string.punctuation + "\n\xa0«»\t—…" + string.digits + "'‘’"
new_text = ''

for ch in text:
    if ch not in cleaning:
        new_text += ch

from nltk import word_tokenize
#nltk.download('punkt')
text_tokens = word_tokenize(new_text)

from nltk.corpus import stopwords
#nltk.download('stopwords')
english_stopwords = stopwords.words("english")
no_stopwords = ''
for w in text_tokens:
    if w not in english_stopwords:
        no_stopwords = no_stopwords + w + ' '


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

#pip install worldcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text_raw = " ".join(text_lemma)
wordcloud = WordCloud().generate(text_raw)
wordcloud.to_file('wordcloud.png')




