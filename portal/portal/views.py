import os
import csv
import datetime
from os.path import dirname, abspath
from demo.models import User, Business, Rating
from django.shortcuts import render

def load_business():
	ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))
	filepath = os.path.join(ROOT_DIR, 'dataset/data_business_backend.csv')
	print filepath
	firstline = True
	row_count = 1

	with open(filepath, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if(firstline):
				firstline = False
				continue

			business_id = row[0]
			name = row[1]
			address = row[2]
			city = row[3]
			state = row[4]
			stars = row[5]
			categories = row[6]
			price = (None if row[7] == 'NA' else row[7])									
			restaurant_stars = (None if row[8] == '-1' else row[8])
			bar_stars = (None if row[9] == '-1' else row[9])
			food_stars = (None if row[10] == '-1' else row[10])
			cafe_stars = (None if row[11] == '-1' else row[11])
			movie_theater_stars = (None if row[12] == '-1' else row[12])
			lodging_stars = (None if row[13] == '-1' else row[13])
			night_club_stars = (None if row[14] == '-1' else row[14])
			parking = row[15]
			bus_station = row[16]
			transit_station = row[17]
			university = row[18]

			# load into database
			business = Business(business_id = business_id, name = name, address = address, city = city, state = state, stars = stars, \
				categories = categories, price = price, \
				restaurant_stars = restaurant_stars, bar_stars = bar_stars, food_stars = food_stars, cafe_stars = cafe_stars, \
				movie_theater_stars = movie_theater_stars, lodging_stars = lodging_stars, night_club_stars = night_club_stars, \
				parking = parking, bus_station = bus_station, transit_station = transit_station, university = university)

			business.save()
		
			row_count = row_count + 1
			print row_count

def index(request):
	# load_business()
	return render(request, 'index.html')