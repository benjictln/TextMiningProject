import os
import re
import json
import pandas


mergedFile = open("news_2015", 'w')
# mergedFile = open("test.json", 'w')
mergedFileText = ""

oriFileDir = "../Data/extracted/"


yearwiseFileDir = "../Data/extracted/yearwise"

for filename in os.listdir(oriFileDir):
	file = open(oriFileDir+filename, "r")

	data=json.load(file)

	df = pandas.DataFrame.from_dict(data)
	#df.rename(columns={' time': 'time'}, inplace=True)
	df.columns = ['title', 'author', 'time', 'description', 'body', 'section']
	print(df.columns)
	df['datetime'] = pandas.to_datetime(df['time'])
	df['year'] = df['datetime'].dt.year
	for v in df.items():
		if(v['year']=='2015'):





	fileText = re.sub(r"}\n", r"},\n", fileText)
	lastCommaIdx = fileText.rfind(',')
	fileText = fileText[:lastCommaIdx] + fileText[lastCommaIdx+1:]
	fileText = "[" + fileText + "]"
	newJsonFile = open(jsonKmoocdir+filename+".json", 'w')
	newJsonFile.write(fileText)
	newJsonFile.close()
	try:
		json_object = json.loads(fileText)
		# print "success"
	except ValueError, e:
		print(filename)