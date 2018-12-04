import pprint
import json
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from rake_nltk import Metric, Rake

#todo : in title [WEATHER] -> can extract date/city ??


path_data = "../data/"
names_file_data = []
names_file_data_changed = []

keys = ["title", " author", " time", " description", " body", " section"]
years = ["2015", "2016", "2017"]
labels = ["ORG", "DATE", "PERCENT", "PERSON", "ORDINAL", "CARDINAL", "TIME", "GPE", "NORP", "LANGUAGE", "FAC", "QUANTITY", "LOC", "WORK_OF_ART", "EVENT", "MONEY", "LAW", "PRODUCT"]
important_labels = ["ORG", "DATE", "PERSON", "TIME", "GPE"]
important_labels_2 = ["ORG", "PERSON", "GPE"]
for i in range(8):
    names_file_data.append(path_data + "koreaherald_1517_" + str(i) + ".json")
    names_file_data_changed.append(path_data + "modified_koreaherald_1517_" + str(i) + ".json")
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

pp = pprint.PrettyPrinter(indent=4)

nb_displayed = 0


def isArticleInThisYear(date_article, targeted_year):
    '''
    :param date_article: string of the form: 2015-02-16 12:31:00
    :param targeted_year: string of the form: 2015
    :return: True if same year, False else.
    '''
    return date_article[0:4] == targeted_year


def test():
    #for year in years:
        #print("\n\n\t***\tBEGINNING YEAR " + year + "\t***")
        # for _ in range(1):

        #if year == "2017":  # to remove
    for i in range(len(names_file_data)):
    #for i in range(2):
        with open(names_file_data[i], 'r+') as f:
            data = json.load(f)

            nb_docs = len(data.get(keys[0]))
            event_dict = {}
            event_date_dict = {}
            event_organization_dict = {}
            event_person_dict = {}
            event_geopolitical_entities_dict = {}
            event_probability_dict = {}

            for j in range(nb_docs):
            #for j in range(1000):
                event = ""
                event_date = ""
                date = data.get(keys[2]).get(str(j))
                #if isArticleInThisYear(date, year):
                body = data.get(keys[4]).get(str(j))
                title = data.get(keys[0]).get(str(j))
                event, event_date, event_organization, event_person, event_geopolitical_entities, event_probability = handle_article_4(title, body)
                #handle_article_4(title, body)
                event_dict.update({str(j): event})
                event_date_dict.update({str(j): event_date})
                event_organization_dict.update({str(j): event_organization})
                event_person_dict.update({str(j): event_person})
                event_geopolitical_entities_dict.update({str(j): event_geopolitical_entities})
                event_probability_dict.update({str(j): event_probability})

            with open(names_file_data_changed[i], 'w') as fp:
                data.update({'event': event_dict})
                data.update({'event_date': event_date_dict})
                data.update({'event_organization': event_organization_dict})
                data.update({'event_person': event_person_dict})
                data.update({'event_geopolitical_entities': event_geopolitical_entities_dict})
                data.update({'event_probability': event_probability_dict})
                json.dump(data, fp)


def handle_article_4(title, body):
    global nb_displayed
    doc = nlp(body)
    dates = handle_dates(doc)
    organizations = []
    persons = []
    geopolitical_entities = []
    probability = 0

    # if there was some dates in the article.
    if len(dates) > 0:
        # todo: compare sentences with dates and title -> can it be the event
        # todo : still compare with title.
        sentence, date, weight_date = extract_information_from_dates(body, dates, title)
        if sentence != "" and date != "":
            print("\n\n\t***\tTITLE\tAND\tSENTENCE\tAND\tDATE\t***")
            print(title)
            #print(sentence)
            #print(date)
            # organizations = get_organization(title, body, sentence)
            # organizations = ", ".join(organizations) # to transform as a string.
            organizations = get_for_label(title, body, sentence, "ORG")
            organizations = ", ".join(organizations) # to transform as a string.
            persons = get_for_label(title, body, sentence, "PERSON")
            persons = ", ".join(persons) # to transform as a string.
            geopolitical_entities = get_for_label(title, body, sentence, "GPE")
            geopolitical_entities = ", ".join(geopolitical_entities) # to transform as a string.

            # probability is 0 if not event, 1 if date_weight == 1, 2 if weight inside ]1 , 3[, 3 is up.  MINUS 1 is said is inside the event name
            probability = 1
            if weight_date > 1:
                probability += 1
            if weight_date >= 3:
                probability += 1
            if probability > 0 and "said" in sentence:
                probability -= 1

            #nb_displayed += 1
            #if nb_displayed == 10:
            #    exit(0)

        return sentence, date, organizations, persons, geopolitical_entities, probability
    return "", "", "", "", "", 0


# CAN BE DELETED
def get_organization(title, body, sentence):
    doc = nlp(body)
    organizations = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # if name of entity has part in title (title: Closure of Kaesong complex unilaterally ordered by ex-leader Park: panel ORG: the Kaesong Industrial Complex
            if nb_similar_words_2_sentences(ent.text, title)>1 or nb_similar_words_2_sentences(ent.text, sentence)>1:

                # we want to keep the bigger name describing the organization, if it is already in organizations
                already_added = False

                for i in range(len(organizations)):
                    organization = organizations[i]
                    if str.lower(ent.text) in str.lower(organization):
                        already_added = True
                        break
                    if str.lower(organization) in str.lower(ent.text):
                        organizations[i] = ent.text
                        already_added = True
                        break

                # if was not yet get so we add it
                if not already_added:

                    labels.append(ent.text)
                    print("NEW label: " + ent.label_ + " text: " + ent.text)
    return organizations


def get_for_label(title, body, sentence, label):
    '''

    :param title: title of the article
    :param body: body of the article
    :param sentence: best sentence from rake_nltk and containing data/words in common with title
    :param label: label of entity that we try to extract from articles
    :return: entities that were extracted
    '''
    doc = nlp(body)
    entities_for_label = []
    for ent in doc.ents:
        if ent.label_ == label:
            # if name of entity has part in title (title: Closure of Kaesong complex unilaterally ordered by ex-leader Park: panel ORG: the Kaesong Industrial Complex
            if nb_similar_words_2_sentences(ent.text, title)>1 or nb_similar_words_2_sentences(ent.text, sentence)>1:
                
                # we want to keep the bigger name describing the entitie_for_label, if it is already in entities_for_label
                already_added = False
                for i in range(len(entities_for_label)):
                    entitie_for_label = entities_for_label[i]
                    if str.lower(ent.text) in str.lower(entitie_for_label):
                        already_added = True
                        break
                    if str.lower(entitie_for_label) in str.lower(ent.text):
                        entities_for_label[i] = ent.text
                        already_added = True
                        break

                # if was not yet get so we add it
                if not already_added:
                    entities_for_label.append(ent.text)
                    print("NEW TEXT FOR label: " + ent.label_ + " text: " + ent.text)
    if len(entities_for_label) > 0:
        print(entities_for_label)
    return entities_for_label


# CAN BE DELETED
def get_organization(title, body, sentence):
    doc = nlp(body)
    organization = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # if name of entity has part in title (title: Closure of Kaesong complex unilaterally ordered by ex-leader Park: panel ORG: the Kaesong Industrial Complex
            if nb_similar_words_2_sentences(ent.text, title) > 1 or nb_similar_words_2_sentences(
                    ent.text, title) > 1:
                labels.append(ent.text)
                print("label: " + ent.label_ + " text: " + ent.text)
        if ent.label_ == "PERSON":
            # if name of entity has part in title (title: Closure of Kaesong complex unilaterally ordered by ex-leader Park: panel ORG: the Kaesong Industrial Complex
            if nb_similar_words_2_sentences(ent.text, title) > 1 or nb_similar_words_2_sentences(
                    ent.text, title) > 1:
                labels.append(ent.text)
                print("label: " + ent.label_ + " text: " + ent.text)
        if ent.label_ == "GPE":
            # if name of entity has part in title (title: Closure of Kaesong complex unilaterally ordered by ex-leader Park: panel ORG: the Kaesong Industrial Complex
            if nb_similar_words_2_sentences(ent.text, title) > 1 or nb_similar_words_2_sentences(
                    ent.text, title) > 1:
                labels.append(ent.text)
                print("label: " + ent.label_ + " text: " + ent.text)

# takes into argument a doc and returns the dates present.
# composed of the date and the weight # 1 per apparitions, 0.5 if before 100 characters
def handle_dates(doc):
    dates = []
    #for ent in doc.ents:
        #if ent.label_ == "TIME":
    for ent2 in doc.ents:
        if ent2.label_ == "TIME" or ent2.label_ == "DATE":
            # todo: also check if title could be an event!
            # todo:
            value = 1
            # bonus of 0.5 if was at begining of the text or if is a time or a day of the week
            if ent2.end_char < 100:
                value += 0.5
            if ent2.label_ == "TIME":
                value += 0.5
            else:
                for day in days:
                    if str.lower(day) == str.lower(ent2.label_):
                        value += 0.5
                        break
            was_added = False
            for i in range(len(dates)):
                if str.lower(dates[i][0]) == str.lower(ent2.text):
                    dates[i][1] += value
                    was_added = True
                    break
            if not was_added:
                dates.append([ent2.text, value])
    return dates


def extract_information_from_dates(body, dates, title):
    best_sentences = return_best_sentences_rake_nltk(body, 16)
    for sentence in best_sentences:
        for i in range(len(dates)):
            # if a date is in one of the sentence given by rake_nltk
            if str.lower(dates[i][0]) in str.lower(sentence[1]):
                same_word_title = nb_similar_words_2_sentences(sentence[1], title)
                # if sentence and title linked, can have similar information(?)
                if (same_word_title > 0):
                    #print("\n\n\t***\tTITLE\t***")
                    #print(title)

                    #print("\t***\tDATE WAS FOUND\t***")
                    #print(sentence)
                    #print(dates[i])
                    # print("same word than title = " + str(same_word_title))
                    # todo: maybe handle with the weigh of the dates to choice which date/sentence to extract.
                    return sentence[1], dates[i][0], int(dates[i][1])
                # else, sentence can still be interesting?

    return "", "", 0


# takes into arguments 2 sentences, and return an int: the number of same words #todo: optimize with weight?
def nb_similar_words_2_sentences(sentence1, sentence2):
    nb_same_words = 0
    for word_sentence1 in sentence1.split(" "):
        for word_sentence2 in sentence2.split(" "):
            if str.lower(word_sentence1) == str.lower(word_sentence2):
                # todo: handle weight too?
                nb_same_words += 1
                # print(word_sentence1)
    return nb_same_words


def handle_article_rake_nltk(text, nb_to_display):
    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    r.extract_keywords_from_text(text)
    ranked_words = r.get_ranked_phrases_with_scores()
    pp.pprint(ranked_words[:nb_to_display])  # To get keyword phrases ranked highest to lowest.


def return_best_sentences_rake_nltk(text, threshold):
    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    r.extract_keywords_from_text(text)
    ranked_words = r.get_ranked_phrases_with_scores()
    for i in range(len(ranked_words)):
        if ranked_words[i][0] < threshold:
            return ranked_words[:i]
    return ranked_words


arg = 1
while (arg!=0):
    arg = int(input("Please enter a number (0 to exit): \n"))
    if arg == 0:
        exit(1)
    if arg == 1:
        test()