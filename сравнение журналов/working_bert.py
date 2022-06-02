#pip install transformers
#pip install torchvision
#pip install -U scikit-learn scipy matplotlib
#pip install -qU transformers sentence-transformers
#Код создавался на основе: https://colab.research.google.com/github/pinecone-io/examples/blob/master/semantic_search_intro/sbert.ipynb#scrollTo=3iQl20fqOLwg

import json
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
with open('corpus_magazines.json') as json_file:
    data = json.load(json_file)

spisok = []
for key in data.keys():
    spisok.append(data[key])

#Инициализируем модель высокочастотного трансформатора и токенизатор - используя предварительно обученную модель SBERT.

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

#Токенизируем всех тексты

tokens = tokenizer(spisok,
                   max_length=128,
                   truncation=True,
                   padding='max_length',
                   return_tensors='pt')

#Обрабатываем маркированные тензоры с помощью модели.

outputs = model(**tokens)

embeddings = outputs.last_hidden_state

mask = tokens['attention_mask'].unsqueeze(-1).expand(embeddings.size()).float()

masked_embeddings = embeddings * mask

summed = torch.sum(masked_embeddings, 1)

counted = torch.clamp(mask.sum(1), min=1e-9)

mean_pooled = summed / counted

# convert to numpy array from torch tensor
mean_pooled = mean_pooled.detach().numpy()

# calculate similarities (will store in array)
scores = np.zeros((mean_pooled.shape[0], mean_pooled.shape[0]))
for i in range(mean_pooled.shape[0]):
    scores[i, :] = cosine_similarity(
        [mean_pooled[i]],
        mean_pooled
    )[0]

plt.figure(figsize=(10,10))
labels = data.keys()
sns.heatmap(scores, xticklabels=labels, yticklabels=labels, annot=True)

plt.savefig('comparison.png')
