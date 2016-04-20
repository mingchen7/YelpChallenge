# Row = BusinessiDList
# AttributeList
import pandas as pd
import csv
import numpy as np

Business_path = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API/data_business_ids.csv'
CategoryList_path = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API/UniqueCategories.csv'
Business_Catogory_path = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API/data_business_ids.csv'
Rated_Business = pd.read_table('extracted_review_features.csv',sep = ',', header = 0, usecols = ['business_id'])
Rated_Business = list(pd.unique(Rated_Business['business_id']))
BusinessList = pd.read_table(Business_path, sep=',', usecols=['business_id'])
CategoryList = pd.read_table(CategoryList_path , sep=',')

CategoryMatirx = pd.DataFrame(index = Rated_Business , columns=CategoryList['0'])
CategoryMatirx = CategoryMatirx.fillna(0)

with open(Business_Catogory_path) as f:
    reader = csv.reader(f)
    next(reader, None)
    chars_to_remove = [' ', '[', ']', '\'']
    for row in reader:
        Business_index = row[0]
        if Business_index in Rated_Business:
            Categories = row[4].translate(None, ''.join(chars_to_remove)).split(',')
            for j in range(len(Categories)):
                if Categories[j] != 'Restaurants' and Categories[j] != 'Food':
                    CategoryMatirx[Categories[j]][Business_index]= 1


CategoryMatirx.to_csv('Business_Catogory_Matirx.csv')

