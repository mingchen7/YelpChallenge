import csv
import pandas as pd
# path = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API/CategoryList.csv'
path = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API/data_business_ids.csv'
# with open(path) as f:
#     reader = csv.reader(f)
#     for row in reader:
#

# with open(path) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print row[0] #define column name wanted to read from csv file
# print row[0]

raw_categories = pd.read_table(path,sep =',',usecols = ['business_id','categoies'])
List = []
chars_to_remove = [' ','[',']','\'']
Rated_Business = pd.read_table('extracted_review_features.csv',sep = ',', header = 0, usecols = ['business_id'])
Rated_Business = list(pd.unique(Rated_Business['business_id']))

for i in range(len(raw_categories)):
    if raw_categories['business_id'][i] in Rated_Business:   # A = raw_categories.loc[i].split('['','', '','']')
        tmp_Categories = raw_categories['categoies'][i]\
                                   .translate(None,''.join(chars_to_remove))
        tmp_Categories = tmp_Categories\
                                   .split(',')
        for j in range(len(tmp_Categories)):
            if tmp_Categories[j] in List:
                continue
            else:
                List.append(tmp_Categories[j])

List = pd.DataFrame(List)
List.to_csv('UniqueCategories.csv')