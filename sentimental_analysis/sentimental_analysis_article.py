# набор данных, на котором будет происходить обучение и проверка модели - Large Movie Review by Эндрю Маасом.
# https://ai.stanford.edu/~amaas/data/sentiment/

!tar xvzf aclImdb_v1.tar.gz

import os

def fetch_reviews(path):
  data = []
  files = [f for f in os.listdir(path)]
  for file in files:
    with open(path+file, "r", encoding='utf8') as f:
      data.append(f.read())
    return data

import pandas as pd

df_train_pos = pd.DataFrame({'review': fetch_reviews('aclImdb/train/pos/'), 'label': 'pos'})
df_train_neg = pd.DataFrame({'review': fetch_reviews('aclImdb/train/neg/'), 'label': 'neg'})

df_test_pos = pd.DataFrame({'review': fetch_reviews('aclImdb/test/pos/'), 'label': 'pos'})
df_test_neg = pd.DataFrame({'review': fetch_reviews('aclImdb/test/neg/'), 'label': 'neg'})

df = pd.concat([df_train_pos, df_train_neg, df_test_pos, df_test_neg], ignore_index=True)


import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = stopwords.words('english') 
stop_words.remove('not') 
lemmatizer = WordNetLemmatizer()

def data_preprocessing(review):
    review = re.sub(re.compile('<.*?>'), '', review) 
    review =  re.sub('[^A-Za-z0-9]+', ' ', review)
    review = review.lower()
    tokens = nltk.word_tokenize(review)
    review = [word for word in tokens if word not in stop_words]
    review = [lemmatizer.lemmatize(word) for word in review]
    review = ' '.join(review)
    return review


df['preprocessed_review'] = df['review'].apply(lambda review: data_preprocessing(review))
df.head()

words_list_pos = df[df['label']=='pos']['preprocessed_review'].unique().tolist()
pos_words = " ".join(words_list_pos)
words_list_neg = df[df['label']=='neg']['preprocessed_review'].unique().tolist()
neg_words = " ".join(words_list_neg)

# здесь на вход подаётся необработанная статья
from bs4 import BeautifulSoup
import string
import nltk

file = open('FILE_NAME', "r", encoding="utf-8") # выбрать нужный файл
contents = file.read()
file.close()
soup = BeautifulSoup(contents, 'lxml')
html_free = soup.get_text('\n', strip='True')
text = html_free.lower()
cleaning = string.punctuation + "\n\xa0«»\t—…" + string.digits + "'‘’"
new_text = ''

for ch in text:
    if ch not in cleaning:
        new_text += ch

from nltk import word_tokenize
text_tokens = word_tokenize(new_text)

from nltk.corpus import stopwords
english_stopwords = stopwords.words("english")
no_stopwords = ''
for w in text_tokens:
    if w not in english_stopwords:
        no_stopwords = no_stopwords + w + ' '


import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(no_stopwords)

lemmatization = []

for token in doc:
    lemmatization.append(token.lemma_)

text_lemma = nltk.Text(lemmatization)

from nltk.probability import FreqDist
fdist = FreqDist(text_lemma)
# если файл был заранее обработан, можно начинать от сюда
words_in_file = " ".join(fdist.keys())

listA = (pos_words.split(" "))
listB = (neg_words.split(" "))
listC = (words_in_file.split(" "))
setA = set(listA)
setB = set(listB)
setC = set(listC)
overlap1 = setA & setC
overlap2 = setB & setC
uni1 = setA | setC
uni2 = setB | setC
pos_rew = float((len(overlap1))/len(uni1)*100)
neg_rew = float((len(overlap2))/len(uni2)*100)
if pos_rew > neg_rew:
    print ("Текст имеет скорее положительную окраску.")
elif pos_rew < neg_rew:
    print ("Текст имеет скорее негативную окраску.")
else:
    print ("Текст имеет скорее нейтральную окраску.")
