########### try spacy ############
# pip install spacy
# python -m spacy download en_core_web_sm

#import spacy
#
## Load English tokenizer, tagger, parser, NER and word vectors
#nlp = spacy.load('en_core_web_sm')
#
## Process whole documents
#text = (u"When Sebastian Thrun started working on self-driving cars at "
#        u"Google in 2007, few people outside of the company took him "
#        u"seriously. “I can tell you very senior CEOs of major American "
#        u"car companies would shake my hand and turn away because I wasn’t "
#        u"worth talking to,” said Thrun, now the co-founder and CEO of "
#        u"online higher education startup Udacity, in an interview with "
#        u"Recode earlier this week.")
#doc = nlp(text)
#for sent in doc.sents:
#    print(sent.text)
#    for token in sent:
#        print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])
#        #print(token.orth_, token.pos_)
#
## Find named entities, phrases and concepts
#for entity in doc.ents:
#    print(entity.text, entity.label_)
#
## Determine semantic similarities
#doc1 = nlp(u"my fries were super gross")
#doc2 = nlp(u"such disgusting fries")
#similarity = doc1.similarity(doc2)
#print(doc1.text, doc2.text, similarity)
############### end spacy##############

########## try lda ############
#import numpy as np
#import lda
#import lda.datasets
#X = lda.datasets.load_reuters()
#vocab = lda.datasets.load_reuters_vocab()
#titles = lda.datasets.load_reuters_titles()
#X.shape
#X.sum()
#model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
#model.fit(X)  # model.fit_transform(X) is also available
#topic_word = model.topic_word_  # model.components_ also works
#n_top_words = 8
#for i, topic_dist in enumerate(topic_word):
#    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
#    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
###############  end lda #############

############### try topic modeling ###############

#from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
#from nltk.stem.porter import PorterStemmer
#from gensim import corpora, models
#import gensim
#
#tokenizer = RegexpTokenizer(r'\w+')
#
## create English stop words list
#en_stop = get_stop_words('en')
#
## Create p_stemmer of class PorterStemmer
#p_stemmer = PorterStemmer()
#
## create sample documents
#doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
#doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
#doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
#doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
#doc_e = "Health professionals say that brocolli is good for your health."
#
## compile sample documents into a list
#doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
#
## list for tokenized documents in loop
#texts = []
#
## loop through document list
#for i in doc_set:
#
#    # clean and tokenize document string
#    raw = i.lower()
#    tokens = tokenizer.tokenize(raw)
#
#    # remove stop words from tokens
#    stopped_tokens = [i for i in tokens if not i in en_stop]
#
#    # stem tokens
#    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
#
#    # add tokens to list
#    texts.append(stemmed_tokens)
#
## turn our tokenized documents into a id <-> term dictionary
#dictionary = corpora.Dictionary(texts)
#
## convert tokenized documents into a document-term matrix
#corpus = [dictionary.doc2bow(text) for text in texts]
#
## generate LDA model
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
#print(ldamodel.print_topics(num_topics=2, num_words=6))
############ end topic modeling ############

##############   try topic modeling by year in one data file #########
import json
import pandas as pd
import os
import re

##### for test LDA first #####
# from nltk.tokenize import RegexpTokenizer
# from stop_words import get_stop_words
# from nltk.stem.porter import PorterStemmer
# from gensim import corpora, models
# import gensim
#
# tokenizer = RegexpTokenizer(r'\w+')
#
# # create English stop words list
#en_stop = get_stop_words('en')
#
# # Create p_stemmer of class PorterStemmer
# p_stemmer = PorterStemmer()
##### for test LDA first #######

##### for 2nd LDA test ######
import datetime
from datetime import timedelta
import nltk
#nltk.download()     # for 1st run
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
'exec(%matplotlib inline)'
from pprint import pprint
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

fileDir = "../Data/extracted/"
mergedFile_18 = "../Data/mergedFile_for_2017.json"     # boi
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

with open(mergedFile_18, 'r') as f:
    data = json.load(f)
    df = pd.DataFrame.from_dict(data)
total_rows = len(df.index)
print(total_rows)

doc_list_2018 = []

temp_doc = ""

for i in range(total_rows):
    news = df.iloc[i]
    #if("2017" in news.loc[' time']):
    #print("time in mergedFile_17: ", news.loc[' time'])
    temp_doc = news.loc[' title'] + news.loc[' body'] + news.loc[' section']
    doc_list_2018.append(temp_doc)

# for doc in doc_list_2018:
#    print("\n", doc,"\n")

doc_list_2018 = [re.sub('\S*@\S*\s?', '', sent) for sent in doc_list_2018]
doc_list_2018 = [re.sub('\s+', ' ', sent) for sent in doc_list_2018]
doc_list_2018 = [re.sub("\'", "", sent) for sent in doc_list_2018]
#pprint(doc_list_2018[:2])

doc_list_2018_words = list(sent_to_words(doc_list_2018))

bigram = gensim.models.Phrases(doc_list_2018_words, min_count=5, threshold=100) # higher threshold fewer phrases.
#bigram_phraser = Phraser(bigram)
#tokens_ = bigram_phraser[sentence_stream]
# tokens_ = bigram_phraser[sentence_stream]
# trigram = Phrases(tokens_, min_count=2, threshold=2, delimiter=b' ')
# trigram_phraser = Phraser(trigram)
# tokens__ = trigram_phraser[tokens_]
# all_words = [i for j in tokens__ for i in j
trigram = gensim.models.Phrases(bigram[doc_list_2018_words], threshold=100)
# trigram_phraser = Phraser(trigram)
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

#print(trigram_mod[bigram_mod[doc_list_2018_words[0]]])

doc_list_2018_words_nostops = remove_stopwords(doc_list_2018_words)
doc_list_2018_words_bigrmas = make_bigrams(doc_list_2018_words_nostops)
nlp = spacy.load('en', disable=['parser', 'ner'])
doc_list_2018_lemmatized = lemmatization(doc_list_2018_words_bigrmas, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
#print(doc_list_2018_lemmatized[:1])

id2word = corpora.Dictionary(doc_list_2018_lemmatized)
texts = doc_list_2018_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]
#print(corpus[:1])
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=15,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
#pprint(lda_model.print_topics())
#for i in range(0, lda_model.num_topics-1):
#model_topics = lda_model.show_topics(formatted=False)
#pprint(lda_model.print_topics(num_words=10))
doc_lda = lda_model[corpus]
visualisation = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.save_html(visualisation, 'LDA_Visualization_2017.html')    # boi

# Compute Perplexity
#print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
# coherence_model_lda = CoherenceModel(model=lda_model, texts=doc_list_2018_lemmatized, dictionary=id2word, coherence='c_v')
# coherence_lda = coherence_model_lda.get_coherence()
#print('\nCoherence Score: ', coherence_lda)

#print(len(corpus))

def format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=doc_list_2018):
    sent_topics_df = pd.DataFrame()

    for i, row in enumerate(lda_model[corpus]):
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = lda_model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break

    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=doc_list_2018)
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
# Show
#df_dominant_topic.head(10)

df_dominant_topic.to_json("../Data/topics_for_2017.json")     # boi

# Group top 5 sentences under each topic
sent_topics_sorteddf_mallet = pd.DataFrame()

sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)],
                                            axis=0)

# Reset Index
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

# Format
sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]

# Show
#sent_topics_sorteddf_mallet.head()

sent_topics_sorteddf_mallet.to_json("../Data/dominent_documnets_for_topics_for_2017.json")    #   boi


# Number of Documents for Each Topic
topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
#print("\ntopic counts = ", topic_counts,"\n")

# Percentage of Documents for Each Topic
topic_contribution = round(topic_counts/topic_counts.sum(), 3)

# Topic Number and Keywords
topic_num_keywords = sent_topics_sorteddf_mallet[['Topic_Num', 'Keywords']]

# Concatenate Column wise
df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)

# Change Column names
df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']

# Show
#df_dominant_topics = df_dominant_topics.sort_values(by='Num_Documents', ascending=False)
df_dominant_topics.to_json("../Data/topic_distribution_for_2017.json")   #      boi

####     for one time only ######
originalFile = mergedFile_18
topicForeachDocumentFile = "../Data/topics_for_2017.json"        # boi
topicGroupbyDocumentFile = "../Data/topic_distribution_for_2017.json"      # boi

originalFileP = open(originalFile, 'r')
topicForeachDocumentFileP = open(topicForeachDocumentFile, 'r')
topicGroupbyDocumentFileP = open(topicGroupbyDocumentFile, 'r')

topicGroupbyData = json.load(topicGroupbyDocumentFileP)
topicForeachDocumentData = json.load(topicForeachDocumentFileP)
originalData = json.load(originalFileP)

topicGroupbyDataDF = pd.DataFrame.from_dict(topicGroupbyData)
topicForeachDocumentDataDF = pd.DataFrame.from_dict(topicForeachDocumentData)
originalDataDF = pd.DataFrame.from_dict(originalData)

topicGroupbyDataDF = topicGroupbyDataDF.sort_values(by='Num_Documents', ascending=False)   # issue by number of documents

topicGroupbyDataDF_total_rows = len(topicGroupbyDataDF.index)
topicForeachDocumentDataDF_total_rows = len(topicForeachDocumentDataDF.index)
originalDataDF_total_rows = len(originalDataDF.index)

newtopicGroupbyDataDF = pd.DataFrame()

currentTopic = 0
datetimeFormat = '%Y-%m-%d %H:%M:%S'
latestArticleTime = '2000-04-16 10:01:28'
oldestArticleTime = '3000-04-16 10:01:28'

for i in range(topicGroupbyDataDF_total_rows):
    topicinfoGroupby = topicGroupbyDataDF.iloc[i]
    currentTopic = topicinfoGroupby.loc['Dominant_Topic']
    currentKeyword = topicinfoGroupby.loc['Topic_Keywords']
    currentNoDoc = topicinfoGroupby.loc['Num_Documents']
    currentTopicContr = topicinfoGroupby.loc['Perc_Documents']
    #print ("Current topic = ", currentTopic)
    #print(news.loc['Dominant_Topic']," ", news.loc['Num_Documents'])
    for j in range(topicForeachDocumentDataDF_total_rows):
        documentInfo = topicForeachDocumentDataDF.iloc[j]
        tempTopic = documentInfo.loc['Dominant_Topic']
        #print ("temp topic = ", tempTopic)
        if (currentTopic == tempTopic):
            originalDocInfo = originalDataDF.iloc[j]
            originalArticleTime = originalDocInfo.loc[' time']
            if(originalArticleTime < oldestArticleTime):
                oldestArticleTime = originalArticleTime
            else:
                latestArticleTime = originalArticleTime
    survivalTime = datetime.datetime.strptime(latestArticleTime, datetimeFormat)- datetime.datetime.strptime(oldestArticleTime, datetimeFormat)
    newtopicGroupbyDataDF = newtopicGroupbyDataDF.append(pd.Series([int(currentTopic), currentKeyword, currentNoDoc, currentTopicContr, survivalTime.days]), ignore_index=True)

newtopicGroupbyDataDF.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents', 'Survival_time_days']
#survivalTime = datetime.datetime.strptime(latestArticleTime, datetimeFormat)- datetime.datetime.strptime(oldestArticleTime, datetimeFormat)
#print(newtopicGroupbyDataDF[''])
newtopicGroupbyDataDF.to_json("../Data/test_2017.json")    # boi

total_no_of_doc = 0
total_survival_time_days = 0
with open("../Data/test_2017.json", 'r') as f:       # boi
     data = json.load(f)
     df = pd.DataFrame.from_dict(data)

total_rows = len(df.index)
print(total_rows)
#sortedTopicbyDocandTime = df.sort_values(by=['Num_Documents', 'Survival_time_days'], ascending=[False, False])
sortedTopicbyDocandTime = df.sort_values(by=['Survival_time_days', 'Num_Documents'], ascending=[False, False])

for i in range(total_rows):
    n = sortedTopicbyDocandTime.iloc[i]
    total_no_of_doc = total_no_of_doc + n.loc['Num_Documents']
    total_survival_time_days = total_survival_time_days + n.loc['Survival_time_days']
    #print("total_no_of_doc ", total_no_of_doc, " and total_survival_time_days = ", total_survival_time_days)
    #print(n.loc['Dominant_Topic']," and keywords = ", n.loc['Topic_Keywords'])
    #print("topic no: ", n.loc['Dominant_Topic'], " and no. of documents = ", n.loc['Num_Documents'], " and survival time = ", n.loc['Survival_time_days'])
    #print("topic no: ", n.loc['Dominant_Topic'], " and survival time = ", n.loc['Survival_time_days'], " and no. of documents = ", n.loc['Num_Documents'])

f.close()
avg_no_of_doc = total_no_of_doc/total_rows
avg_survival_time = total_survival_time_days/total_rows
print("avg_no_of_doc = ", avg_no_of_doc, " and avg_survival_time = ", avg_survival_time)

with open("../Data/test_2017.json", 'r') as f:       # boi
     data = json.load(f)
     df = pd.DataFrame.from_dict(data)

total_rows = len(df.index)
print(total_rows)

newtopicGroupbyDataDF = pd.DataFrame()

for i in range(total_rows):
    suddenChangeFlag = 0
    n = df.iloc[i]
    currentTopic = n.loc['Dominant_Topic']
    currentKeyword = n.loc['Topic_Keywords']
    currentNoDoc = n.loc['Num_Documents']
    currentTopicContr = n.loc['Perc_Documents']
    currentSurvivalTime = n.loc['Survival_time_days']
    if(n.loc['Num_Documents']>avg_no_of_doc and n.loc['Survival_time_days']<avg_survival_time):
        suddenChangeFlag = 1
    newtopicGroupbyDataDF = newtopicGroupbyDataDF.append(pd.Series([int(currentTopic), currentKeyword, currentNoDoc, currentTopicContr, currentSurvivalTime, suddenChangeFlag]), ignore_index=True)
newtopicGroupbyDataDF.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents', 'Survival_time_days', 'SuddenChangeFlag']
newtopicGroupbyDataDF.to_json("../Data/test_2017_withFlag.json")    # boi

f.close()
#####     for one time only ######

with open("../Data/test_2015_withFlag.json", 'r') as f:       # boi
     data = json.load(f)
     df = pd.DataFrame.from_dict(data)

total_rows = len(df.index)
print(total_rows)
#sortedTopicbyDocandTimeandFlag = df.sort_values(by=['Num_Documents'], ascending=[False])        # sort by number of doc
#sortedTopicbyDocandTimeandFlag = df.sort_values(by=['Survival_time_days','Num_Documents'], ascending=[False, False])    # sort by time, doc
#sortedTopicbyDocandTimeandFlag = df.sort_values(by=['Survival_time_days'], ascending=[False])        # sort by survival time
sortedTopicbyDocandTimeandFlag = df.sort_values(by=['SuddenChangeFlag', 'Survival_time_days', 'Num_Documents'], ascending=[False, False, False])    # sort by all 3

for i in range(total_rows):
    n = sortedTopicbyDocandTimeandFlag.iloc[i]
    #print("\ntopic no: ", n.loc['Dominant_Topic'],"  keywords: ", n.loc['Topic_Keywords'], " Topic name: ", n.loc['Topic_name'], " no of doc: ", n.loc['Num_Documents'])     #  # sort by number of doc
    #print("  keywords: ", n.loc['Topic_Keywords'], " Topic name: ", n.loc['Topic_name'], " time: ", n.loc['Survival_time_days'], "doc: ", n.loc['Num_Documents'])  # sort by time, doc
    print("  keywords: ", n.loc['Topic_Keywords'], " Topic name: ", n.loc['Topic_name'], " Flag: ", n.loc['SuddenChangeFlag'], " time: ", n.loc['Survival_time_days'], "doc: ", n.loc['Num_Documents'])  # sort by all 3


#######     issue for event ######
eventFileP = open("../Data/eventInfoFile2015.json", 'w')        # boi
topicForeachDocumentFile = "../Data/topics_for_2015.json"           # boi
topicForeachDocumentFileP = open(topicForeachDocumentFile, 'r')
mergedFile_18 = "../Data/mergedFile_for_2015.json"                  # boi

with open("../Data/test_2015_withFlag.json", 'r') as f:             # boi
     topic_name_data = json.load(f)
     topic_name_dataDF = pd.DataFrame.from_dict(topic_name_data)

with open(mergedFile_18, 'r') as f:
     merged_name_data = json.load(f)
     merged_name_data = pd.DataFrame.from_dict(merged_name_data)

# Data_Path = "../Data/extracted/koreaherald_1517_{}.json"
# for fileId in range(8):
#     with open(Data_Path.format(fileId), 'r') as f:
#         data = json.load(f)
#         if fileId == 0:
#             oridf = pd.DataFrame.from_dict(data)
#         else:
#             oridf = oridf.append(pd.DataFrame.from_dict(data))
#
# total_rows_ori = len(oridf.index)
# print("Original file lenth: ", total_rows_ori)

Data_Path = "../Data/modified_koreaherald_1517_{}.json"
for fileId in range(8):
    with open(Data_Path.format(fileId), 'r') as f:
        data = json.load(f)
        if fileId == 0:
            df = pd.DataFrame.from_dict(data)
        else:
            df = df.append(pd.DataFrame.from_dict(data))

total_rows = len(df.index)
print("Modified file length: ",total_rows)

eventInfoDF = pd.DataFrame()

topic_info = json.load(topicForeachDocumentFileP)
topicForeachDocumentFileP.close()
topic_info_df = pd.DataFrame.from_dict(topic_info)

count = 0
count_in_text = 0
for i in range(total_rows):
    n = df.iloc[i]
    if("2015" in n.loc[' time'] and n.loc['event']!=""):        # boi
        count = count+1
        #print("\nevent no: ", count)
        #print("time ", n.loc[' time'], " and event ", n.loc['event'])
        news_body_of_event = n.loc[' body']
        #print("\nbody of the event: ", news_body_of_event)
        #### test ###
        for j in range(len(merged_name_data.index)):
            n1 = merged_name_data.iloc[j]
            if(news_body_of_event in n1.loc[' body']):
                count_in_text = count_in_text+1
                #print("\nevent found in mergedfile: ", count_in_text)
                #print("body in event: \n", news_body_of_event, "\nbody in merged file: ", n1.loc[' body'], " and time: ", n1.loc[' time'])
                topic_no = topic_info_df.get('Dominant_Topic').get(str(j))
                #print("topic no: ", topic_no)
                for k in range(len(topic_name_dataDF.index)):
                    if (topic_no == topic_name_dataDF.iloc[k].loc['Dominant_Topic']):
                        print("Topic no: ", topic_no, " and topic name: ", topic_name_dataDF.iloc[k].loc['Topic_name'], " event: ", n.loc['event'])
                        eventInfoDF = eventInfoDF.append(pd.Series([n.loc['event'], news_body_of_event, topic_name_dataDF.iloc[k].loc['Topic_name']]), ignore_index=True)
                        break
                break
print("total event in 2015: ", count)
print("And total found in ori: ", count_in_text)
eventInfoDF.columns = ['Event', 'Article_body', 'Topic_name']
eventInfoDF.to_json(eventFileP)
eventFileP.close()
    ##### test #####
        # for j in range(len(topic_info_df.index)):
        #     n1 = topic_info_df.iloc[j]
        #     if(news_body_of_event in n1.loc['Text']):
        #         count_in_text = count_in_text+1
        #         print("\nevent found in docfile: ", count_in_text)
        #         print("body in event: \n", news_body_of_event, "\nbody in doc file: ", n1.loc['Text'])
        #         break;
        #         topic_no = n1.loc['Dominant_Topic']
        #         for k in range(len(topic_name_dataDF.index)):
        #            if (topic_no == topic_name_dataDF.iloc[k].loc['Dominant_Topic']):
        #                print("Topic no: ", topic_no, " and topic name: ", topic_name_dataDF.iloc[k].loc['Topic_name'], " event: ", n.loc['event'])
        #         eventInfoDF = eventInfoDF.append(pd.Series([n.loc['event'], n.loc[' body'], topic_name_dataDF.iloc[k].loc['Topic_name']]), ignore_index=True)
    ##### test ######

###  Issue for event ###
