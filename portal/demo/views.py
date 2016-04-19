from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from demo.models import User, Business, Rating
import datetime
import hashlib
import random
import json

def user(request):
	context = {
		'id': 'user'
	}	
	return render(request, 'demo/user.html', context)	

def business(request, page_num=1):
	# take random 9 restaurants
	index_list = range(0,5667)
	rnd_list = random.sample(index_list, 9)	

	context = {}
	context['page'] = int(page_num)
	
	rest_id = 1
	for rnd in rnd_list:
		business = Business.objects.all()[rnd]		
		info = {}
		info['restaurant_id'] = business.id
		info['name'] = business.name
		info['address'] = business.address
		info['business_id'] = business.business_id
		context[rest_id] = info
		rest_id = rest_id + 1
	
	# print json.dumps(context, indent = 2)
	return render(request, 'demo/business.html', context)

def detail(request, restaurant_id):
	# print restaurant_id
	business = Business.objects.get(pk = restaurant_id)		

	# parsing the categories string
	s = business.categories
	s = s[1:len(s)-1]
	s = s.split(',')
	categories_list = []
	for category in s:
		category = category.split()	 # trimming string
		category = category[0][1:-1] # remove quotes
		categories_list.append(category)		
	
	# print business.restaurant_stars
	# print type(business.restaurant_stars)
	context = {
		'business_id': business.business_id,
		'name': business.name,
		'address': business.address,
		'city': business.city,
		'state': business.state,
		'stars': business.stars,
		'categories': business.categories,
		'price': business.price,
		'restaurant_stars': ("" if business.restaurant_stars == None else "%.1f" % business.restaurant_stars),
		'bar_stars': ("" if business.bar_stars == None else "%.1f" % business.bar_stars),
		'cafe_stars': ("" if business.cafe_stars == None else "%.1f" % business.cafe_stars),
		'movie_theater_stars': ("" if business.movie_theater_stars == None else "%.1f" % business.movie_theater_stars),
		'lodging_stars': ("" if business.lodging_stars == None else "%.1f" % business.lodging_stars),
		'night_club_stars': ("" if business.night_club_stars == None else "%.1f" % business.night_club_stars),
		'parking': business.parking,
		'bus_station': business.bus_station,
		'transit_station': business.transit_station,
		'university': business.university
	}

	if business.price != None:
		price_list = range(business.price)
	else:
		price_list = []

	stars_list = range(int(business.stars))
	empty_stars_list = range(5 - int(business.stars))
 	context['price_list'] = price_list
 	context['stars_list'] = stars_list
 	context['empty_stars_list'] = empty_stars_list
 	context['categories_list'] = categories_list

	return render(request, 'demo/detail.html', context)

def recommendation(request):
	context = {}
	return render(request, 'demo/recommendation.html', context)

def register(request):
	try:
		# register a new user
		sys_time = str(datetime.datetime.now())
		hash_md5 = hashlib.md5(sys_time)		
		hash_pwd = hashlib.md5(request.POST['password'])

		user_id = hash_md5.hexdigest()
		username = request.POST['username']
		email = request.POST['email']		
		encoded_pwd = hash_pwd.hexdigest()

		print user_id
		print request.POST['username']
		print request.POST['email']
		print request.POST['password']
		print encoded_pwd
		user = User(user_id = user_id, name = username, email = email, password = encoded_pwd)
		user.save()		

	except KeyError:
		render(request, 'demo/user.html', {
			'error_message': "Username has already existed!"
			})

	# redirect back to businesses page
	else:
		# reverse to business page 1
		return HttpResponseRedirect(reverse('demo:business', args = (1,)))


