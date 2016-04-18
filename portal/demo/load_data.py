import os
import csv
import datetime
import hashlib
from os.path import dirname, abspath
from models import User, Business, Rating


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
			categoires = row[6]
			price = row[7]
			restaurant_stars = row[8]
			bar_stars = row[9]
			food_stars = row[10]
			cafe_stars = row[11]
			movie_theater_stars = row[12]
			lodging_stars = row[13]
			night_club_stars = row[14]
			parking = row[15]
			bus_station = row[16]
			transit_station = row[17]
			university = row[18]

			print business_id,name,address,city,state

			row_count = row_count + 1
			if(row_count > 20):
				break