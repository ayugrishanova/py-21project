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
words_list_pos = df[df['label']=='pos']['preprocessed_review'].unique().tolist()
pos_words = " ".join(words_list_pos)
words_list_neg = df[df['label']=='neg']['preprocessed_review'].unique().tolist()
neg_words = " ".join(words_list_neg)


#pip install wordcloud 
#conda install -c conda-forge wordcloud

# Positive Reviews Wordcloud from IMDb

from wordcloud import WordCloud

words_list = df[df['label']==1]['preprocessed_review'].unique().tolist()
pos_words = " ".join(words_list)

pos_wordcloud =  WordCloud(
                  width=800, height = 500,            
                  stopwords=stop_words).generate(pos_words)

plt.figure(figsize=(8, 8), facecolor = None)
plt.imshow(pos_wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

# Negative Reviews Wordcloud from IMDb

words_list = df[df['label']==0]['preprocessed_review'].unique().tolist()
neg_words = " ".join(words_list)

neg_wordcloud =  WordCloud(
                  width=800, height = 500,            
                  stopwords=stop_words).generate(neg_words)

plt.figure(figsize=(8, 8), facecolor = None)
plt.imshow(neg_wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
