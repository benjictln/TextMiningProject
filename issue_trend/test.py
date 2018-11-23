import json
from rake_nltk import Metric, Rake
import pprint
import sys
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
            with open(names_file_data[i], 'r') as f:
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


def test3(argv):
    if argv == 4:
        r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO, min_length=1, max_length=2)
    elif argv == 5:
        r = Rake(ranking_metric=Metric.WORD_DEGREE, min_length=1, max_length=2)
    elif argv == 6:
        r = Rake(ranking_metric=Metric.WORD_FREQUENCY, min_length=1, max_length=2)
    elif argv == 7:
        r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    elif argv == 8:
        r = Rake(ranking_metric=Metric.WORD_DEGREE)
    elif argv == 9:
        r = Rake(ranking_metric=Metric.WORD_FREQUENCY)
    else:
        r = Rake(min_length=1, max_length=2)  # Uses stopwords for english from NLTK, and all puntuation characters.
    for year in years:
        if year == "2017": # to remove
            #for i in range(len(names_file_data)):
            for i in range(2):
                with open(names_file_data[i], 'r') as f:
                    data = json.load(f)

                    nb_docs = len(data.get(keys[0]))
                    #for j in range(nb_docs):
                    for j in range(10):
                        date = data.get(keys[2]).get(str(j))
                        if isArticleInThisYear(date, year):
                            body = data.get(keys[4]).get(str(j))
                            r.extract_keywords_from_text(body)
                            pp.pprint(r.get_ranked_phrases_with_scores()[:6])  # To get keyword phrases ranked highest to lowest.
                            section = data.get(keys[5]).get(str(j))
                            print(section)

# min_length=2, max_length=4
#r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
#
#

#test3()

arg = 1

while (arg!=0):
    arg = int(input("Please enter a number (0 to exit): \n"))
    if arg == 1:
        test1()
    elif arg == 2:
        test2()
    elif arg >= 3:
        test3(arg)

