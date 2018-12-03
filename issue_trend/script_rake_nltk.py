import json
import pandas
path_data = "../data/"
names_file_data = []
for i in range(8):
    names_file_data.append(path_data + "koreaherald_1517_" + str(i) + ".json")


def get_primary_tags(f):
    '''
    :param f: file that contains the json
    :return: the main attributes
    '''
    datas = json.load(f)
    attributes = []
    for data in datas:
        print(data)
        attributes.append(data)
    return (attributes)


for i in range(len(names_file_data)):
    if (i==0):
        with open( names_file_data[i], 'r') as f:
            datas=json.load(f)
            for tag_main in datas:
                print(len(tag_main))
                print(tag_main)
                for tag_min in datas[tag_main]:
                    intermediate_data = datas[tag_main]
                    print("ONE DATA IN " + str(tag_main))
                    print(intermediate_data[tag_min])

            #df = pandas.DataFrame.from_dict(data)
            #dtypes = df.dtypes
            #print(len(dtypes))
            #print(dtypes)
            #values = dtypes.values
            #print(values)
            #print df.values
            #for j in dtypes:
                #print(type(j))
                #print(len(j))
                #print(str(j))
