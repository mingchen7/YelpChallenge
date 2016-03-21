# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 01:57:00 2016

@author: Wan
"""


import numpy as np
import scipy as sp
import pylab as pl
import pandas as pd
import nltk
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from numpy import *

# read in csv file, first header for the first line by default
r = pd.read_csv('C:/Users/Wan/Desktop/510/yelp data/yelp_academic_dataset_review.csv',
                nrows = 5,
                usecols = ["text"])

for title in r:
    print title

print r



sid = SentimentIntensityAnalyzer()

for row in r["text"]:
    sentences = row
    print sentences

    ss = sid.polarity_scores(sentences)
    print ss
    print







