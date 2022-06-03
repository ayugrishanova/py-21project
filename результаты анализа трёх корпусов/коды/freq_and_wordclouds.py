def prepared(text):
    
    import spacy
    import nltk

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    lemmatization = []
    for token in doc:
        lemmatization.append(token.lemma_)

    text_lemma = nltk.Text(lemmatization)

    from nltk.probability import FreqDist
    fdist = FreqDist(text_lemma)
    most_common_words = fdist.most_common(50)
 
    return most_common_words, text_lemma

from wordcloud import WordCloud
import matplotlib.pyplot as plt

filename = str(input('Введите название файла с корпусом: '))
stops=str(input('Напишите фамилию и формы имени актора, которые могут часто встречаться, с маленькой буквы через пробел: '))
stops_list=stops.split()

import json

file = open(filename, 'r', encoding='utf-8')
tg_dict=json.load(file)
file.close()

freq_dict = dict()
for t in tg_dict:
    freq = prepared(tg_dict[t])
    freq_dict.update({ t : freq[0] })
    text_raw = " ".join(freq[1])
    wordcloud = WordCloud(width=1000, height=1000, stopwords = stops_list, background_color = "#fff5ee", colormap = "tab10").generate(text_raw)
    cloudname = t + '.png'
    wordcloud.to_file(cloudname)

with open("corpus.json", "w") as write_file:
    json.dump(freq_dict, write_file)
