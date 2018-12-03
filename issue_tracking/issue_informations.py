import pprint
from snips_nlu import load_resources, SnipsNLUEngine

import io
import json
# for initialization of Snips
load_resources(u"en")
nlu_engine = SnipsNLUEngine()
with io.open("./sample_dataset.json") as f:
    sample_dataset = json.load(f)
    nlu_engine.fit(sample_dataset)



path_data = "../data/"
names_file_data = []
keys = ["title", " author", " time", " description", " body", " section"]
years = ["2015", "2016", "2017"]


threshold = 4

for i in range(8):
    names_file_data.append(path_data + "koreaherald_1517_" + str(i) + ".json")



pp = pprint.PrettyPrinter(indent=4)


def isArticleInThisYear(date_article, targeted_year):
    '''
    :param date_article: string of the form: 2015-02-16 12:31:00
    :param targeted_year: string of the form: 2015
    :return: True if same year, False else.
    '''
    return date_article[0:4] == targeted_year



def test():
    global idf, wordsThatAppeared, wordsDocumentFrequency, nbOfFiles
    for year in years:
    #for _ in range(1):
        idf = []

        if year == "2017":  # to remove
            for i in range(len(names_file_data)):
            #for i in range(1):
                with open(names_file_data[i], 'r') as f:
                    data = json.load(f)
                    nb_docs = len(data.get(keys[0]))
                    #for j in range(nb_docs):
                    for j in range(1):
                        date = data.get(keys[2]).get(str(j))
                        if isArticleInThisYear(date, year):
                            body = data.get(keys[4]).get(str(j))
                            for line in body.split("."):
                                parsing = nlu_engine.parse(unicode(line.encode("utf-8").decode("utf-8")))
                                if parsing["intent"] != None:
                                    print(json.dumps(parsing, indent=2))
                            #parsing = nlu_engine.parse(body)
                            #parsing = nlu_engine.parse(u"What will be the weather in San Francisco next week?")
                            #print(json.dumps(parsing, indent=2))

def test2():
    global idf, wordsThatAppeared, wordsDocumentFrequency, nbOfFiles
    for year in years:
    #for _ in range(1):
        idf = []

        if year == "2017":  # to remove
            for i in range(len(names_file_data)):
            #for i in range(1):
                with open(names_file_data[i], 'r') as f:
                    data = json.load(f)
                    nb_docs = len(data.get(keys[0]))
                    #for j in range(nb_docs):
                    for j in range(1000):
                        date = data.get(keys[2]).get(str(j))
                        if isArticleInThisYear(date, year):
                            title = data.get(keys[0]).get(str(j))
                            parsing = nlu_engine.parse(unicode(title))
                            if parsing["intent"] != None:
                                print(json.dumps(parsing, indent=2))




arg = 1
while (arg!=0):
    arg = int(input("Please enter a number (0 to exit): \n"))
    if arg == 0:
        exit(1)
    if arg == 1:
        test()
