# Term project proposal
Team 6 : Benjamin Castellan, Jibon Naher, Liu Zhao-Yang
## Problem definition 

The huge amount of information is generated every day and is impossible for a human to read them all. Even the reporters who contributed their working time summarizing the events that happened in the world can not completely know the trend in every field. Therefore, we apply the computers to help us understand the trend in the world. In this project, we will focus on two important problems of news mining: issue trend analysis and issue tracking. We try to find the hot issue and event relationship in a fixed period news dataset. The issue trend analysis is to detect the top popular issues every year and the issue tracking is to determine the relation between events belonging to a specific issue.
To solve these two problems, we need to define the issue and event first clearly. The definition of an issue is a term composed of multiple words and mentioned by at least K news articles in the dataset. An event is a subject(S) + Verb(V) + Object(O) or Verb(V) + Object(O) pair that occurred in the news article. Therefore, a news article will contain one issue, one major event it talks about and other events which it mentions.
Issue trend analysis
In this task, we try to extract trend issues from a set of issues. We think the trend issue should satisfy three features: high discussion, long surviving time and sudden emerging. If an issue is discussed many times, it is more popular. Hence, we will try to count the number of discussion for the issue. Second, a trend issue will survive for a long time rather than being a flash in the pan. The period of discussion is also an important feature for a trend issue. We will take the issues with longer discussion time as the trend issues. The last feature is sudden emerging which will consider the discussion frequency and time together.  If the discussion degree of an issue change severely, there might be some significant events happening. Therefore, we will monitor the discussion degree of the issue during the time and extract the issue with dramatic change as a trend issue.
Issue tracking
After we find the trend issues, we can further investigate the event relation in the trend issue and the detail of the events. We divide the relation into two types, follow-up events or independent events. The follow-up events are the events happening one by one and being related. If an event is mentioned by a news article and isn’t the major event, the event is related to the major event. The happening time of these two events will be the basis of deciding the order of the relation. The independent events are the events never mentioned by news articles except for their own news. We will also extract the details of the events such as the place, the time, the person(s) and organization by utilizing Named-entity recognition(NER) techniques.
 


## Ideas & approaches

Concerning the issue trend analysis, we will first try to found the issues. In order to do so, we will gather the most important terms for each document, using either a method as term discrimination value or tf * idf or using a tool like rake-nltk (described below). Because the title often contains important words and summarize the article but can also be too vague to extract an issue from it, we will apply the different methods on the title only, the title and the body, and the body only to determine which part gives us the best result. 
To determine the top trend issues, we will try a mix between the number of articles, the "surviving time" of an issue and the suddenly increase in frequency and select the combination that gives us the most compelling results. The surviving time is calculated from the written time of the first news to the last news belonging to the issue. The ways to detect the sudden increase in frequency is to define a threshold and check the change is above the threshold or not.

Concerning the issue tracking, we have some ideas about how to find follow-up events. One idea would be to find an event that is mentioned in another article. We could also compare the most important words (as we did to find the trends above) and 2 articles with many important words in common, such as name entities and place entities, but different date, we can assume they are related.

We will use python because it is the easiest language to use, known by all the group members and because many libraries are available. Some tools that we could use are rake-nltk (https://pypi.org/project/rake-nltk/ ) which provides an algorithm that determine key phrases in a text, snips-nlu (https://github.com/snipsco/snips-nlu ) that is a NLU engine that extracts important pieces of information like a place or a date. Another tool we could use is Stanford CoreNLP ( https://stanfordnlp.github.io/CoreNLP/ ), which provides functions like a part-of-speech tagger, a named entity recognizer or a sentiment analysis tool. Finally, we could also use IEPY ( https://github.com/machinalis/iepy ) which gives information extraction capabilities focused on relation extraction.

## Related work

There are some existing works to effectively identify emerging news issue. Normally, particular attributes for emerging issues are identified manually. In [1], the authors proposed an approach to identify an emerging issue with high quality and performance. They proposed three pruning strategy. First one is impact based pruning which ensures that the emerging issue impact a large number of people. Second is related to significant volume increase of the issue since most of the time an emerging issue increase in a large volume in a short time. The third one is isolation pruning which is needed to remove the redundancy of issues. 

After finding the issues, identifying the most important event of a particular news article is also a tedious job. In [2], authors worked on identifying the most prominent event of a news article. They did an experiment on existing method of finding event by gold event coreference relations. They found that as well as this relations, some subevent relation analysis can give a better result.

## References
“iDice: Problem Identification for Emerging Issues”, Qingwei Lin Jian-Guang Lou Hongyu Zhang Dongmei Zhang, https://dl.acm.org/citation.cfm?id=2884795
“Identifying the Most Dominant Event in a News Article by Mining Event Coreference Relations”, Prafulla Kumar Choubey, Kaushik Raju, Ruihong Huang, https://aclanthology.coli.uni-saarland.de/papers/N18-2055/n18-2055

## Prefessor consulting session
* Only using the POS tag with SVO and VO pairs are not enough to find all events.
* Finding following and independent events by matching the words or synonyms is too simple. Therefore, we should add more constraints to define the event types
