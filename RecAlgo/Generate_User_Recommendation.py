import pandas as pd
import numpy as np
from sklearn.externals import joblib
import GenerateUserProfile

def Generate_Recommendation(RatingUserFile):
    RatingUserRecords = pd.read_table(RatingUserFile, sep=',')
    User = RatingUserRecords['user'][0]

    Business_List = pd.read_table('BusinessID_List.csv',sep = ',')
    Business_List = list(Business_List['0'])

    RatingResults = pd.DataFrame(0, index=[User], columns=Business_List)
    for index in range(len(RatingUserRecords['business_id'])):
        RatingResults[RatingUserRecords['business_id'][index]][User] = RatingUserRecords['stars'][index]

    Business_Tag = pd.read_table('Business_Tag_Log.csv', sep=',', header=0, index_col=0)
    User_tag = RatingResults.dot(Business_Tag)
    User_tag = GenerateUserProfile.Scale_and_normalization(User_tag,'model/scaler/User_Tag_Robust_scaler')

    RatingUserRecords = None

    diff = np.multiply(Business_Tag, User_tag)
    svr = joblib.load('model/svr/svr_linear_10.pkl')
    res = svr.predict(diff)
    res = pd.DataFrame(res, index=Business_List)
    res = list(res.sort(columns=[0], ascending=False)[0:5].index)

    return res



print Generate_Recommendation('rating_demo_dataframe.csv')