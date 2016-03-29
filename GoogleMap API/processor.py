import json
import time
import pymongo
import csv
import os
import logging
import datetime


class Processor:
	LOG_FILE = 'process.log'

	def __init__(self):
	    # set up logging configuration
	    logging.basicConfig(filename = self.LOG_FILE, level = logging.DEBUG)    	

	def extractFeature(self, categories_all, categories_rating):
		firstline = True
		count_places = {}
		ratings = {}
		row_count = 1
	 	header = ['business_id','restaurant','bar','shopping_mall','food','cafe','grocery_or_supermarket','movie_theater','lodging','night_club', \
                  'parking','bus_station','subway_station','transit_station','university','school', \
                  'restaurant_min', 'restaurant_avg','restaurant_max', \
                  'bar_min', 'bar_avg', 'bar_max', \
                  'food_min', 'food_avg', 'food_max', \
                  'cafe_min', 'cafe_avg', 'cafe_max', \
                  'movie_theater_min', 'movie_theater_avg','movie_theater_max', \
                  'lodging_min', 'lodging_avg', 'lodging_max', \
                  'night_club_min', 'night_club_avg', 'night_club_max']

		with open('googlemap_features.csv', 'a') as f_write:
			writer = csv.writer(f_write)
			writer.writerow(header)


		with open('Dataset_Phoenix_Restaurants.csv', 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				if(firstline):
					firstline = False
					continue

				business_id = row[0]
				print "row #%d: %s" % (row_count, business_id)
				logging.debug(business_id)

				logging.debug("Extracting number of places...")
				for category in categories_all:
					# find the # of places of given business id and category							
					logging.debug("%s, %s" % (business_id, category))
					count = self.place_count(business_id, category)								
					count_places[category] = count					

				logging.debug("Extrating ratings...")
				for category in categories_rating:					
					logging.debug("%s, %s" % (business_id, category))
					# find the (min, avg, max) of ratings for the given business id and category
					aggr = self.aggregate_ratings(business_id, category)					
					logging.debug(aggr)
					ratings[category] = aggr
				
				with open('googlemap_features.csv', 'a') as f_write:
					writer = csv.writer(f_write)
					# construct a line to write
					line = []
					line.append(business_id)
					for category in categories_all:
						line.append(count_places[category])

					for category in categories_rating:
						line.extend(ratings[category])
					writer.writerow(line)

				logging.debug("\n")
				row_count = row_count + 1
                
				# if(row_count >= 5): break			
	
	def place_count(self, business_id, category):
		try:
			client = pymongo.MongoClient()
			db = client.googlemap
			
		except pymongo.errors.ConnectionFailure, e:
		    print "Could not connect to server: %s" % e

		cursor = db.places.find({"yelp_id" : business_id, "place_type": category})
		client.close()
		return cursor.count()															

	def aggregate_ratings(self, business_id, category):
		try:
			client = pymongo.MongoClient()
			db = client.googlemap

		except pymongo.errors.ConnectionFailure, e:
		    print "Could not connect to server: %s" % e

		min_rating = 99
		max_rating = 0
		avg_rating = 0
		sum_rating = 0
		count = 0

		# no places found
		cursor = db.places.find({"yelp_id" : business_id, "place_type": category})
		if cursor.count() == 0:
			return [-1, -1, -1]

		for document in cursor:
			if 'rating' in document:				
				rating = document['rating']
				sum_rating = sum_rating + rating
				count = count + 1

				if rating <= min_rating:
					min_rating = rating

				if rating >= max_rating:
					max_rating = rating

			else:								
				logging.debug("The restaurant %s does not have rating!" % document['name'])
						
		if count == 0: 
			return [-1, -1, -1]						
		
		avg_rating = sum_rating / count

		client.close()
		return [min_rating, avg_rating, max_rating]


if __name__ ==	"__main__":
	categories_all = ('restaurant','bar','shopping_mall','food','cafe','grocery_or_supermarket','movie_theater','lodging','night_club', \
                  'parking','bus_station','subway_station','transit_station','university','school')			
	categories_rating = ('restaurant','bar','food','cafe','movie_theater','lodging','night_club')
	Processor().extractFeature(categories_all, categories_rating)


