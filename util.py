import re, nltk, pickle, pandas as pd
from os import listdir, path
from nltk.stem import WordNetLemmatizer
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def cleanContext(context = None):
    pattern = re.compile('[^A-Za-z]+')
    context = re.sub(r'\S*@\S*\s?', '', context)
    context = nltk.word_tokenize(context)
    CleanContext = []
    wordnetlemma = WordNetLemmatizer()
    for word in context:
        word = word.lower()
        word = wordnetlemma.lemmatize(word)
        cleanWord = pattern.sub('', word)
        if len(cleanWord)>0:
            CleanContext.append(cleanWord)
    return CleanContext

def SavePickle(FileName = None, Data = None):
    pickle.dump(Data, open('./PreCalculated_Data/{}.pkl'.format(FileName), 'wb'))
    return

def LoadPickle(FileName = None):
    data = pickle.load(open('./PreCalculated_Data/{}.pkl'.format(FileName), 'rb'))
    return data

def find_ngrams(input_list, n):
    if n % 2 == 0:
        print("n need to be odd!")
        return
    else:
        if len(input_list) < n:
            return [tuple(input_list)]*(n-1)
        else:
            times = int(n/2)
            ngramList = list(zip(*[input_list[i:] for i in range(n)]))
            NewngramList = ngramList
            # add firt word and last word pair
            for t in range(times):
                NewngramList = [ngramList[0][:-(t+1)]] + NewngramList
                NewngramList.append(ngramList[-1][(t+1):])
            return NewngramList

# Calculate TfIdf
# def CalculateTfIdf(corpus = None):
#     vectorizer = CountVectorizer(tokenizer=lambda text: nltk.word_tokenize(text))
#     transformer = TfidfTransformer()
#     X = vectorizer.fit_transform(corpus)
#     tfidf = transformer.fit_transform(X)
#     weight = tfidf.toarray()
#     vocabulary = vectorizer.get_feature_names()
#     # print()
#     return weight, vocabulary

# if __name__ == "__main__":
#     for dataset in ['baseball', 'hockey']:
#         Text_file = '.\\20news-bydate\\rec.sport.{}'.format(dataset)
#         AllNews = read_News(directory = Text_file)
#         print(AllNews.shape)
#         SavePickle(FileName = 'All{}NewsPdSeries'.format(dataset), Data = AllNews)
#     print(AllNews.shape)
#     print(AllNews.head())
#     print(AllNews.index)
#     print(AllNews.values)

