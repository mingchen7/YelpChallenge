from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
	# id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length = 32)
	name = models.CharField(max_length = 40, null = True)
	email = models.CharField(max_length = 40)
	password = models.CharField(max_length = 32)

	def __str__(self):
		return self.name

class Business(models.Model):
	## yelp features
	# id = models.AutoField(primary_key=True)
	business_id = models.CharField(max_length = 32)
	name = models.CharField(max_length = 100)
	address = models.CharField(max_length = 100)
	city = models.CharField(max_length = 20)
	state = models.CharField(max_length = 10)
	stars = models.FloatField()
	categories = models.CharField(max_length = 200)
	price = models.IntegerField(null = True)

	## google map place features
	# rating is aggregated using avg
	restaurant_stars = models.FloatField(null = True)
	bar_stars = models.FloatField(null = True)
	food_stars = models.FloatField(null = True)
	cafe_stars = models.FloatField(null = True)
	movie_theater_stars = models.FloatField(null = True)
	lodging_stars = models.FloatField(null = True)
	night_club_stars = models.FloatField(null = True)

	# count of places
	parking = models.IntegerField(null = True)
	bus_station = models.IntegerField(null = True)
	transit_station = models.IntegerField(null = True)
	university = models.IntegerField(null = True)

	def __str__(self):
		return "%s, %s" % (self.name, self.address)

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	business = models.ForeignKey(Business, on_delete = models.CASCADE)
	stars = models.IntegerField(default = 0)

	def __str__(self):
		return "%s, %s, %d" % (self.user, self.business, self.stars)

