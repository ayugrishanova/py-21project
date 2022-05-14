from nltk import ngrams
from collections import Counter

file_out = open('out.txt','w')
file_in = open('test.txt')

for line in file_in:
    text = line.split()
bi_grams = list(ngrams(text, 2))
bi_grams = Counter(bi_grams).most_common(3)
print(bi_grams)
file_out.close()
file_in.close()