  # Row = BusinessiDList
# AttributeList
import pandas as pd
import AddNewRatings as ad
import csv
import numpy as np


def Countrows(filename):           # return number of rows
    num_lines = sum(1 for line in open(filename))
    return num_lines

RatingfilePath = 'extracted_review_features.csv'
header = list(pd.read_table(RatingfilePath,sep = ',', header = 0, nrows = 0).columns.values)
RatingLines = Countrows(RatingfilePath)
Rated_Business = pd.read_table('extracted_review_features.csv',sep = ',', header = 0, usecols = ['business_id'])
Rated_Business = list(pd.unique(Rated_Business['business_id']))

Rated_User= pd.read_table('extracted_review_features.csv',sep = ',', header = 0, usecols = ['user_id'])
Rated_User= list(pd.unique(Rated_User['user_id']))

RatingMatrixPath = 'C:/Users/rui/Documents/GitHub/YelpChallenge/GoogleMap API\RatingMatrix.csv'
chunksize = 1000

RatingMatrix = pd.DataFrame(index = Rated_User, columns=Rated_Business)
RatingMatrix = RatingMatrix.fillna(0)

# Check if busness in our list
# 3.if all in set that value to the matirx.
# 4. Next Step
for i in range(1, RatingLines, chunksize):
    Ratings = pd.read_table(RatingfilePath,
            sep = ',',# no header, define column henader manually later
            header = None,
            nrows=chunksize, # number of rows to read at each iteration
            skiprows=i)   # skip rows that were already read
    Ratings.columns = header
    Ratings= Ratings[['user_id', 'business_id', 'rating']]
    for index in Ratings.index:
        RatingMatrix[Ratings['business_id'][index]][Ratings['user_id'][index]] = Ratings['rating'][index]
        print i,index

RatingMatrix.to_csv('RatingMatrix.csv')





