import json
import pandas as pd
import os

mergedFile_18 = "../Data/mergedFile_for_2018.json"
mergedFile_17 = "../Data/mergedFile_for_2017.json"
mergedFile_16 = "../Data/mergedFile_for_2016.json"
mergedFile_15 = "../Data/mergedFile_for_2015.json"

# article_dict_2018 = {
#             " title":[],
#             " author":[],
#             " time":[],
#             " description":[],
#             " body": [],
#             " section": []
#             }
# article_dict_2017 = {
#             " title":[],
#             " author":[],
#             " time":[],
#             " description":[],
#             " body": [],
#             " section": []
#             }
# article_dict_2016 = {
#             " title":[],
#             " author":[],
#             " time":[],
#             " description":[],
#             " body": [],
#             " section": []
#             }
article_dict_2015 = {
            " title":[],
            " author":[],
            " time":[],
            " description":[],
            " body": [],
            " section": []
            }

Data_Path = "../Data/extracted/koreaherald_1517_{}.json"
for fileId in range(8):
    with open(Data_Path.format(fileId), 'r') as f:
        data = json.load(f)
        if fileId == 0:
            df = pd.DataFrame.from_dict(data)
        else:
            df = df.append(pd.DataFrame.from_dict(data))

total_rows = len(df.index)
for i in range(total_rows):
   news = df.iloc[i]
   # if("2018" in news.loc[' time']):
   #     article_dict_2018[' title'].append(news.loc['title'])
   #     article_dict_2018[' author'].append(news.loc[' author'])
   #     article_dict_2018[' time'].append(news.loc[' time'])
   #     article_dict_2018[' description'].append(news.loc[' description'])
   #     article_dict_2018[' body'].append(news.loc[' body'])
   #     article_dict_2018[' section'].append(news.loc[' section'])
    # elif("2017" in news.loc[' time']):
    #    article_dict_2017[' title'].append(news.loc['title'])
    #    article_dict_2017[' author'].append(news.loc[' author'])
    #    article_dict_2017[' time'].append(news.loc[' time'])
    #    article_dict_2017[' description'].append(news.loc[' description'])
    #    article_dict_2017[' body'].append(news.loc[' body'])
    #    article_dict_2017[' section'].append(news.loc[' section'])
   # elif("2016" in news.loc[' time']):
   #     article_dict_2016[' title'].append(news.loc['title'])
   #     article_dict_2016[' author'].append(news.loc[' author'])
   #     article_dict_2016[' time'].append(news.loc[' time'])
   #     article_dict_2016[' description'].append(news.loc[' description'])
   #     article_dict_2016[' body'].append(news.loc[' body'])
   #     article_dict_2016[' section'].append(news.loc[' section'])
   if("2015" in news.loc[' time']):
       article_dict_2015[' title'].append(news.loc['title'])
       article_dict_2015[' author'].append(news.loc[' author'])
       article_dict_2015[' time'].append(news.loc[' time'])
       article_dict_2015[' description'].append(news.loc[' description'])
       article_dict_2015[' body'].append(news.loc[' body'])
       article_dict_2015[' section'].append(news.loc[' section'])

json = json.dumps(article_dict_2015)
f = open(mergedFile_15,"w")
f.write(json)
f.close()
