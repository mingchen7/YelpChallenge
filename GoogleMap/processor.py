import json
import time
import pymongo
import csv
import os
import logging
import datetime


class Processor:

	def extractFeature(self, category_all, category_rating):
		firstline = True
		count_places = {}
		ratings = 
		with open('Dataset_Phoenix_Restaurants.csv', 'rb') as f:
			reader = csv.reader()
			for row in reader:
				if(firstline):
					firstline = False
					continue

				business_id = row[0]


if __name__ ==	"__main__":
	category_all = ('restaurant','bar','shopping_mall','food','cafe','grocery_or_supermarket','movie_theater','lodging','night_club', \
                  'parking','bus_station','subway_station','transit_station','university','school')			
	category_rating = ('restaurant','bar','food','cafe','movie_theater','lodging','night_club')
	Processor().extractFeature(category_all, category_rating)


