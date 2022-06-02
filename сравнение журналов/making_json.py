import os

user_path=str(input('Введите путь: '))
filelist = []
for root, dirs, files in os.walk(user_path): 
    for file in files: 
        filelist.append(os.path.join(root,file)) 

list_articles = dict()

for n in range(len(filelist)):
    file = open(filelist[n], 'r')
    text = file.read()
    name = filelist[n].split('/')
    magazine = name[len(name)-1]
    list_articles.update({ magazine : text })

import json

with open("corpus_magazines.json", "w") as write_file:
    json.dump(list_articles, write_file)