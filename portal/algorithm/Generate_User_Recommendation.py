import pandas as pd
import numpy as np
import os
import GenerateUserProfile
from sklearn.externals import joblib
from os.path import dirname, abspath

def Generate_Recommendation(RatingUserRecords):        
    ROOT_DIR = dirname(dirname(abspath(__file__)))
    print ROOT_DIR

    User = RatingUserRecords['user'][0]

    file_business = os.path.join(ROOT_DIR, 'algorithm/BusinessID_List.csv')
    Business_List = pd.read_table(file_business, sep = ',')
    Business_List = list(Business_List['0'])

    RatingResults = pd.DataFrame(0, index=[User], columns=Business_List)
    for index in range(len(RatingUserRecords['business_id'])):
        RatingResults[RatingUserRecords['business_id'][index]][User] = RatingUserRecords['stars'][index]

    file_tag = os.path.join(ROOT_DIR, 'algorithm/Business_Tag_Log.csv')
    Business_Tag = pd.read_table(file_tag, sep=',', header=0, index_col=0)
    User_tag = RatingResults.dot(Business_Tag)

    file_scaler = os.path.join(ROOT_DIR, 'algorithm/User_Tag_Robust_scaler')
    User_tag = GenerateUserProfile.Scale_and_normalization(User_tag, file_scaler)
    RatingUserRecords = None

    file_model = os.path.join(ROOT_DIR, 'algorithm/svc_linear_100.pkl')
    diff = np.multiply(Business_Tag, User_tag)
    svr = joblib.load(file_model)
    res = svr.predict_proba(diff)
    res = pd.DataFrame(res, index=Business_List)
    print res.sort(columns=[1], ascending=False)
    res = list(res.sort(columns=[1], ascending=False)[0:5].index)

    return res



