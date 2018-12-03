import json, pandas as pd, nltk, time, itertools, pprint, util
from operator import itemgetter

## POS faster

# dfSmall.loc['title_Tokensize'] = dfSmall.apply(lambda row: nltk.word_tokenize(row['title']), axis=1)
# dfSmall.loc['body_Tokensize'] = dfSmall.apply(lambda row: nltk.word_tokenize(row[' body']), axis=1)
#
# dfSmall.loc['title_POS'] = dfSmall.apply(lambda row: nltk.pos_tag(row['title_Tokensize']), axis=1)
# dfSmall.loc['body_POS'] = dfSmall.apply(lambda row: nltk.pos_tag(row['body_Tokensize']), axis=1)

# Start = time.time()
# df['title_Tokensize'] = df.apply(lambda row: nltk.word_tokenize(row['title']), axis=1)
# df['body_Tokensize'] = df.apply(lambda row: nltk.word_tokenize(row[' body']), axis=1)
# Finish = time.time()
# print(Finish-Start)

# Start = time.time()
# body = df['title_Tokensize'].values
# title = df['body_Tokensize'].values
# title_Tag = nltk.pos_tag_sents(title)
# body_Tag = nltk.pos_tag_sents(body)
# Finish = time.time()
# print(Finish-Start)

## Generate every possible pairs of ('NN', 'VB'), ('VB', 'NN'), ('NN','JJ'), ('JJ', 'NN'), ('NN', 'VB', 'NN')

def generateEventTagPair(sentence):
    PossibleTagCombination = [('NN', 'VB'), ('VB', 'NN'), ('NN','JJ'), ('JJ', 'NN')] # ('NN', 'VB', 'NN'),
    PossibleTag = ['NN', 'VB', 'JJ']
    IndexList = {}
    for Tag in PossibleTag:
        index = []
        for i, word in enumerate(sentence):
            if Tag in word[1] and len(word[0]) > 1: #remove the word only contains one character
                index.append(i)
        IndexList[Tag]=index
    Output = []
    for PTC in PossibleTagCombination:
        AllC = itertools.product(*[IndexList[T] for T in PTC])
        AllC = [C for C in AllC if C[0] < C[1]]
        Output.append(AllC)
    ## Generate ('NN', 'VB', 'NN') pairs
    TriplePairs = []
    for P1 in Output[0]:
        for P2 in Output[1]:
            if P1[1] == P2[0]:
                TriplePairs.append((P1[0], P1[1], P2[1]))
    Output.insert(0, TriplePairs)
    Output = [item for item in Output if len(item) > 0]

    for i, item in enumerate(Output):
        NewItem = []
        for pair in item:
            pair = [sentence[index] for index in pair]
            NewItem.append(pair)
        Output[i] = NewItem
    # Flatten the list
    Output = list(itertools.chain(*Output))
    return Output

# Calculate pair score by IfIdf
def calculatePairScore(Pair, Dict):
    score = 0
    for w in Pair:
        # w[0] = w[0].lower()
        if w[0].lower() not in Dict:
            print("{} not in the dictionary".format(w[0]))
            continue
        score += Dict[w[0].lower()]
    score = score/len(Pair)
    return score

if __name__ == '__main__':
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    pp = pprint.PrettyPrinter(indent=4)
    dict = {}
    TopK = 10
    ## Load data

    Data_Path = "./data/koreaherald_1517_{}.json"
    for fileId in range(1):
        with open(Data_Path.format(fileId), 'r') as f:
            data = json.load(f)
            if fileId == 0:
                df = pd.DataFrame.from_dict(data)
            else:
                df = df.append(pd.DataFrame.from_dict(data))

    ## Calculate and Save TfIdf

    # rowIndex = df.index.values
    #
    # corpus = df[' body'].values
    # weight, vocabulary = util.CalculateTfIdf(corpus=corpus)
    # for i, ind in zip(range(len(weight)), rowIndex):
    #     tempDict = {}
    #     for j in range(len(vocabulary)):
    #         if weight[i][j] > 0:  # and word[j] not in tempDict
    #             tempDict[vocabulary[j]] = weight[i][j]
    #         # else:
    #         #     print("Duplicate Word!")
    #     dict[ind] = tempDict
    #
    # util.SavePickle("TfIdf", dict)

    # Load TfIdf
    dict = util.LoadPickle("TfIdf")

    ## Get Smaller data

    dfSmall = df[:3]

    ## print Event
    for id in range(dfSmall.shape[0]):
        news = dfSmall.iloc[id]
        print(news)
        # TStart = time.time()
        Sentences = tokenizer.tokenize(news.loc[' body'])
        text = [nltk.word_tokenize(s) for s in Sentences]
        q = nltk.pos_tag_sents(text)
        e = []
        for w in q:
            e.extend(generateEventTagPair(w))
        for i, pair in enumerate(e):
            e[i].append(calculatePairScore(pair, dict[news.name]))
        e = sorted(e, key=itemgetter(-1), reverse=True)
        print("Top {} result:".format(TopK))
        pp.pprint(e[:TopK])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(e)
        # TFinish = time.time()
        # print(TFinish-TStart)



