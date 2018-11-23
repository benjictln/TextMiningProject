import json
from rake_nltk import Metric, Rake
import pprint

path_data = "../data/"
names_file_data = []
keys = ["title", " author", " time", " description", " body", " section"]

for i in range(8):
    names_file_data.append(path_data + "koreaherald_1517_" + str(i) + ".json")

r = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.

pp = pprint.PrettyPrinter(indent=4)

def test1():
    for i in range(len(names_file_data)):
        if i == 0:
            with open( names_file_data[i], 'r') as f:
                data = json.load(f)
                #df = pandas.DataFrame.from_dict(data)
                #print(df)
                nb_docs = len(data.get(keys[0]))
                for i in range(1):

                    body = data.get(keys[4]).get(str(i))
                    r.extract_keywords_from_text(body)
                    pp.pprint(r.get_ranked_phrases_with_scores())  # To get keyword phrases ranked highest to lowest.

def test2():
    bigBody = ""
    with open( names_file_data[0], 'r') as f:
        data = json.load(f)
        #df = pandas.DataFrame.from_dict(data)
        #print(df)
        nb_docs = len(data.get(keys[0]))
        for i in range(10):
            print("TEXT NB:" + str(i))

            body = data.get(keys[4]).get(str(i))
            bigBody += body
            #print( data.get(keys[3]).get(str(i)))

            r.extract_keywords_from_text(body)

            pp.pprint(r.get_ranked_phrases_with_scores()[:2])  # To get keyword phrases ranked highest to lowest.

test2()