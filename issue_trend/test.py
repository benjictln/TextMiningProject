import json
from rake_nltk import Metric, Rake
import pprint

path_data = "../data/"
names_file_data = []
keys = ["title", " author", " time", " description", " body", " section"]
years = ["2015", "2016", "2017"]

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


def nb_of_articles_per_year():
    '''
    This function goes through all the articles and print the number of articles in each year
    '''
    years = []
    nb_in_years = []
    for i in range(len(names_file_data)):
        with open(names_file_data[i], 'r') as f:
            data = json.load(f)
            nb_docs = len(data.get(keys[0]))
            for j in range(nb_docs):
                date_article = data.get(keys[2]).get(str(j))
                year_already_seen = False
                for index_year in range(len(years)):
                    if isArticleInThisYear(date_article,years[index_year]):
                        year_already_seen = True
                        nb_in_years[index_year] += 1
                        break
                if not year_already_seen:
                    years.append(date_article[0:4])
                    nb_in_years.append(1)
    for k in range(len(years)):
        print("The year is " + years[k] + " and the number of article is " + str(nb_in_years[k]) + "\n")


def isArticleInThisYear(date_article, targeted_year):
    '''
    :param date_article: string of the form: 2015-02-16 12:31:00
    :param targeted_year: string of the form: 2015
    :return: True if same year, False else.
    '''
    return date_article[0:4] == targeted_year




nb_of_articles_per_year()
