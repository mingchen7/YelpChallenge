import pandas as pd
import numpy as np
from sklearn import preprocessing
import sklearn as skl
from sklearn.externals import joblib

def Get_User_Preference(User_Business,Business_Tag):
    User_Tag =  User_Business.dot(Business_Tag)
    return User_Tag

def Scale_and_normalization(User_Tag,Scaler_route):
    User_Tag_columns = list(User_Tag.columns)
    User_Tag_index = list(User_Tag.index)
    User_Tag_Robust_scaler = joblib.load(Scaler_route)
    User_Tag = User_Tag_Robust_scaler.transform(User_Tag)
    User_Tag = preprocessing.normalize(User_Tag, norm='l2')
    User_Tag = pd.DataFrame(User_Tag, columns=User_Tag_columns,
                                    index=User_Tag_index
                 )
    return User_Tag


