import json, pandas as pd, nltk, time, itertools, pprint, util, math, networkx as nx, matplotlib.pyplot as plt#, spacy
from operator import itemgetter
from datetime import datetime

if __name__ == '__main__':
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    pp = pprint.PrettyPrinter(indent=4)
    #nlp = spacy.load('en_core_web_lg')
    G = nx.DiGraph()
    TimeFormat = "%Y-%m-%d %H:%M:%S"

    dict = {}
    TopK = 10

    ## Load data

    Data_Path = "./data/modified_koreaherald_1517_{}.json"
    for fileId in range(8):
        with open(Data_Path.format(fileId), 'r') as f:
            data = json.load(f)
            if fileId == 0:
                df = pd.DataFrame.from_dict(data)
            else:
                df = df.append(pd.DataFrame.from_dict(data))

    print(df.info())

    df_event = df.loc[df['event']!='']
    print(df_event.info())

    # Y2016 = datetime.strptime('2016','%Y')
    # Y2017 = datetime.strptime('2017','%Y')

    # for q in range(df_event.shape[0]):
    #     t = datetime.strptime(df_event.iloc[q].loc[' time'], TimeFormat)
    #     if t > Y2016 and t < Y2017:
    #         print(df_event.iloc[q])

    # Check different types in the field
    # temp = df['event_date'].values
    # tD = {}
    # for q in temp:
    #     if type(q).__name__ not in tD:
    #         tD[type(q).__name__] = True
    # print(tD)

    df_eventNp = df_event.values
    df_event_Index = df_event.index.values
    print(df_eventNp.shape)
    for eventId1 in range(len(df_eventNp)):
        tempgeopolitical = set([])
        temporganization = set([])
        tempperson = set([])

        if type(df_eventNp[eventId1][7]) == str and df_eventNp[eventId1][7] != "": tempgeopolitical = set([df_eventNp[eventId1][7]])
        else: tempgeopolitical = set(df_eventNp[eventId1][7])

        if type(df_eventNp[eventId1][8]) == str and df_eventNp[eventId1][8] != "": temporganization = set([df_eventNp[eventId1][8]])
        else: temporganization = set(df_eventNp[eventId1][8])

        if type(df_eventNp[eventId1][9]) == str and df_eventNp[eventId1][9] != "": tempperson = set([df_eventNp[eventId1][9]])
        else: tempperson = set(df_eventNp[eventId1][9])

        for eventId2 in range(eventId1+1,len(df_eventNp)):
            count = 0
            temp2geopolitical = set([])
            temp2organization = set([])
            temp2person = set([])
            if type(df_eventNp[eventId2][7]) == str and df_eventNp[eventId2][7] != "":
                temp2geopolitical = set([df_eventNp[eventId2][7]])
            else:
                temp2geopolitical = set(df_eventNp[eventId2][7])

            if type(df_eventNp[eventId2][8]) == str and df_eventNp[eventId2][8] != "":
                temp2organization = set([df_eventNp[eventId2][8]])
            else:
                temp2organization = set(df_eventNp[eventId2][8])

            if type(df_eventNp[eventId2][9]) == str and df_eventNp[eventId2][9] != "":
                temp2person = set([df_eventNp[eventId2][9]])
            else:
                temp2person = set(df_eventNp[eventId2][9])

            # if df_eventNp[eventId1][6] == df_eventNp[eventId2][6]: count += 1
            if len(tempgeopolitical.intersection(temp2geopolitical)) > 0 : count += 1
            if len(temporganization.intersection(temp2organization)) > 0: count += 1
            if len(tempperson.intersection(temp2person)) > 0: count += 1
            if count > 1:
                # print(df_event.loc[df_event_Index[eventId1],:])
                if df_event_Index[eventId1] not in G:
                    G.add_node(df_event_Index[eventId1], event=df_eventNp[eventId1][5])
                if df_event_Index[eventId2] not in G:
                    G.add_node(df_event_Index[eventId2], event=df_eventNp[eventId2][5])
                Event1_datetime = datetime.strptime(df_eventNp[eventId1][4], TimeFormat)
                Event2_datetime = datetime.strptime(df_eventNp[eventId2][4], TimeFormat)
                if Event1_datetime < Event2_datetime:
                    G.add_edge(df_event_Index[eventId1], df_event_Index[eventId2])
                else:
                    G.add_edge(df_event_Index[eventId2], df_event_Index[eventId1])
                print(df_eventNp[eventId1])
                print(df_eventNp[eventId2])
                print("~~~~~~~~~~我是分隔線~~~~~~~~~~")
            # else:
            #     print(df_eventNp[eventId2])
            #     print("~~~~~~~~~~我是分隔線~~~~~~~~~~")
    print("Number of Event in Follow up relationship {}".format(G.number_of_nodes()))
    print("Number of relationship in Follow up relationship {}".format(G.number_of_edges()))
    nx.draw(G, labels = nx.get_node_attributes(G, 'event'), with_labels=True)
    plt.show()
    # print(df_eventNp[0])
    #
    # for id in range(df_event.shape[0]):
    #     news = df_event.iloc[id]
    #     if type(news.loc['event']) != str:
    #         print(news)


    #
    # ## Get Smaller data
    #
    # dfSmall = df[:3]
    #
    # ## print Event
    # for id in range(dfSmall.shape[0]):
    #     news = dfSmall.iloc[id]
    #     print(news)
    #     # TStart = time.time()
    #     Sentences = tokenizer.tokenize(news.loc[' body'])
    #     text = [nltk.word_tokenize(s) for s in Sentences]
    #     q = nltk.pos_tag_sents(text)
    #     e = []
    #     for w in q:
    #         e.extend(generateEventTagPair(w))
    #     for i, pair in enumerate(e):
    #         e[i].append(calculatePairScore(pair, dict[news.name]))
    #     e = sorted(e, key=itemgetter(-1), reverse=True)
    #     print("Top {} result:".format(TopK))
    #     pp.pprint(e[:TopK])
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     # print(e)
    #     # TFinish = time.time()
    #     # print(TFinish-TStart)



