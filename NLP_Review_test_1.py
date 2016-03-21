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
# first 5 rows
# only review contect selected 
r = pd.read_csv('C:/Users/Wan/Desktop/510/yelp data/yelp_academic_dataset_review.csv',
                nrows = 5,
                usecols = ["text"])


##  check title
for title in r:
    print title    

##  check conents
print r


##  fun to analyze
sid = SentimentIntensityAnalyzer()

##  print comments for each content
for row in r["text"]:
    sentences = row
    print sentences     ##  review content

    ss = sid.polarity_scores(sentences)
    print ss            ##  comments
    print







