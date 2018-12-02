import json
import pandas as pd
import os
import re

#### for test LDA first #####
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

fileDir = "../Data/extracted/"
fileTest = "../Data/extracted/koreaherald_1517_0.json"
mergedFile = open("../Data/mergedFile.json", 'w')

Data_Path = "../Data/extracted/koreaherald_1517_{}.json"
for fileId in range(8):
    with open(Data_Path.format(fileId), 'r') as f:
        data = json.load(f)
        if fileId == 0:
            df = pd.DataFrame.from_dict(data)
        else:
            df = df.append(pd.DataFrame.from_dict(data))

total_rows = len(df.index)
print(total_rows)

doc_list_2018 = []
temp_doc = ""

for i in range(total_rows):
    news = df.iloc[i]
    if("2017" in news.loc[' time']):
        temp_doc = news.loc['title'] + news.loc[' body'] + news.loc[' section']
        doc_list_2018.append(temp_doc)

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_list:

   # clean and tokenize document string
   raw = i.lower()
   tokens = tokenizer.tokenize(raw)

   # remove stop words from tokens
   stopped_tokens = [i for i in tokens if not i in en_stop]

   # stem tokens
   stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

   # add tokens to list
   texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=5)
for i in range(0, ldamodel.num_topics-1):
    print(ldamodel.print_topic(i))
#print(ldamodel.print_topics(num_topics=10, num_words=6))
