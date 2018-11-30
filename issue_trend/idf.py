import json
import pprint
from nltk.tokenize import word_tokenize
import math
path_data = "../data/"
names_file_data = []
keys = ["title", " author", " time", " description", " body", " section"]
years = ["2015", "2016", "2017"]
sections = ["Defense", "", "Politics", "Social affairs", "North Korea",
            "International", "National", "Science", "Foreign  Affairs",
            "Education", "Foreign Policy", "사용안함 - Diplomatic Circuit",
            "사용안함 - Environment", "사용안함 - Sharing", "Diplomatic Circuit"]

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

idf = []
wordsThatAppeared = []
nbOfFiles = 0
wordsDocumentFrequency = []


def calculateIdf():
    global idf, wordsThatAppeared, wordsDocumentFrequency, nbOfFiles
    for i in range(len(wordsThatAppeared)):
        idf.append(math.log(float(nbOfFiles)/float(wordsDocumentFrequency[i]),2))


def orderIdf():
    global idf, wordsThatAppeared
    for i in range(len(idf)):
        for j in range(i+1, len(idf)):
            if idf[i] < idf[j]:
                value_idf = idf[i]
                value_word = wordsThatAppeared[i]
                idf[i] = idf[j]
                wordsThatAppeared[i] = wordsThatAppeared[j]
                idf[j] = value_idf
                wordsThatAppeared[j] = value_word


def test():
    global idf, wordsThatAppeared, wordsDocumentFrequency, nbOfFiles
    for year in years:
    #for _ in range(1):
        idf = []
        wordsThatAppeared = []
        nbOfFiles = 0
        wordsDocumentFrequency = []
        #if year == "2017":  # to remove
        if year == "2017":  # to remove
            for i in range(len(names_file_data)):
            #for i in range(1):
                with open(names_file_data[i], 'r') as f:
                    data = json.load(f)
                    nb_docs = len(data.get(keys[0]))
                    for j in range(nb_docs):
                    #for j in range(1):
                        date = data.get(keys[2]).get(str(j))
                        if isArticleInThisYear(date, year):
                            nbOfFiles += 1
                            body = data.get(keys[4]).get(str(j))
                            words = word_tokenize(body)
                            wordsInThisDocument = []
                            for word in words:
                                wordAlreadySeenInDoc = False
                                for oldWordThisDoc in wordsInThisDocument:
                                    if oldWordThisDoc == word:
                                        # this word was already seen in this document so we just need to ignore it
                                        wordAlreadySeenInDoc = True
                                        break
                                if not wordAlreadySeenInDoc:
                                    wordSeenInAnyDoc = False
                                    for index in range (len(wordsThatAppeared)):
                                        if wordsThatAppeared[index] == word:
                                            # this word was already seen in another document
                                            wordsDocumentFrequency[index] += 1
                                            wordsInThisDocument.append(word)
                                            wordSeenInAnyDoc = True
                                            break
                                    if not wordSeenInAnyDoc:
                                        # word was first seen in this document, add it
                                        wordsThatAppeared.append(word)
                                        wordsDocumentFrequency.append(1)
                                        wordsInThisDocument.append(word)
            calculateIdf()
            orderIdf()
            for i in range(len(wordsThatAppeared)):
                print("Word number: " + str(i+1) + " is: " + wordsThatAppeared[i] + "(idf = " + str(idf[i]) + ").")





arg = 1
while (arg!=0):
    arg = int(input("Please enter a number (0 to exit): \n"))
    if arg == 0:
        exit(1)
    if arg == 1:
        test()
