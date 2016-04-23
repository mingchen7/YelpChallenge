from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from demo.models import User, Business, Rating
import django.db as db
import datetime
import hashlib
import random
import json
import pandas as pd
# import demo.Generate_User_Recommendation as recommend

def user(request):
	context = {
		'cust_id': 1
	}	
	return render(request, 'demo/user.html', context)	

def business(request, page_num=1, cust_id = 1):
	print "In the Business Page. Customer id: %d" % int(cust_id)

	# take random 9 restaurants
	index_list = range(0,5667)
	rnd_list = random.sample(index_list, 9)	

	context = {}
	context['page'] = int(page_num)
	context['cust_id'] = cust_id
	
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

def detail(request, restaurant_id, cust_id):
	print "In the Detail Page. Customer id: %d, Restaurant id: %d" % (int(cust_id), int(restaurant_id))
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

	price_list = [] if business.price == None else range(business.price)	
	stars_list = range(int(business.stars))
	empty_stars_list = range(5 - int(business.stars))
 	context['price_list'] = price_list
 	context['stars_list'] = stars_list
 	context['empty_stars_list'] = empty_stars_list
 	context['categories_list'] = categories_list
 	context['cust_id'] = cust_id
 	context['restaurant_id'] = restaurant_id

 	# determine if already rated
 	user = User.objects.get(pk = cust_id) 	
 	query = Rating.objects.filter(user = user, business = business)
 	star_sequence = ['star1','star2','star3','star4','star5']
 	if len(query) >= 1:
 		rated_star = query[0].stars
 		for i in range(rated_star):
 			context[star_sequence[i]] = True
 		for i in range(rated_star, 5):
 			context[star_sequence[i]] = False 		
 	else:
 		for i in range(5):
 			context[star_sequence[i]] = False

 	print "Query result: %d" % len(query)
	return render(request, 'demo/detail.html', context)

def rating(request, restaurant_id, cust_id, rating):
	print "In the rating page."
	print "restaurant id: %d, customer id: %d, rating: %d" % (int(restaurant_id), int(cust_id), int(rating))

	try:
		user = User.objects.get(pk = cust_id)
		business = Business.objects.get(pk = restaurant_id)
		query = Rating.objects.filter(user = user, business = business)
		# already rated
		if(len(query)) >= 1:			
			raise Http404("This restaurant has already been rated.")			
		# not rated
		else:
			rating = Rating(user = user, business = business, stars = int(rating))
			rating.save()

	except db.Error as e:
		raise Http404(e.message)	
	else:
		# direct back to the business page		
		return HttpResponseRedirect(reverse('demo:business', args = (1, cust_id,)))

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
		
		user = User(user_id = user_id, name = username, email = email, password = encoded_pwd)
		user.save()
		cust_id = user.id		
		print "auto customer id: %d" % cust_id

	except KeyError:
		render(request, 'demo/user.html', {
			'error_message': "Username has already existed!"
			})

	# redirect back to businesses page
	else:
		# reverse to business page 1
		return HttpResponseRedirect(reverse('demo:business', args = (1, cust_id,)))

def recommendation(request, cust_id):
    print "In the Recommendation Page. Customer id: %d" % int(cust_id)

    ## get rated restaurants given cust_id
    user = User.objects.get(pk = cust_id)
    ratingList = Rating.objects.filter(user = user)
    values = ratingList.values('user','business','stars')

    ### construct data matrix as input
    df = pd.DataFrame.from_records(values)
    nrow = len(df['business'])

    business_id_list = ['None'] * nrow
    next_id = ''
    i = 0

    while i < nrow:    	
    	print ratingList[i].business.business_id
        next_id =  str(Business.objects.filter(pk = str(ratingList[i].business_id))[0].business_id)
        print next_id
        business_id_list[i] = next_id
        i = i + 1

    ##   Create a column from the business_id_list
    df['business_id'] = business_id_list

    df_togo = df.drop('business',1)

	# construct results
    # rec_list = recommend.Generate_Recommendation(df_togo)
    rec_list = ['ZZlMGUiKZNiDyPLmra7RZQ','zYRKOiYCZJAg1SV1WZG4lw','ZxGg3JpHVryyPSVpQHdLvQ','ZXcKt050sV4iKXM-BVQgCA','zwHM6hz8swKIG-4-BSKMPA']

    context = {}
    context['cust_id'] = cust_id

    for i in range(len(rec_list)):    	
    	rec_detail = {}
        business_detail = Business.objects.get(business_id = rec_list[i])
        price_list = [] if business_detail.price == None else range(business_detail.price)
        stars_list = range(int(business_detail.stars))
        empty_stars_list = range(5 - int(business_detail.stars))

        rec_detail['id'] = str(business_detail.id)
        rec_detail['name'] = str(business_detail.name)
        rec_detail['address'] = str(business_detail.address)
        rec_detail['business_id'] = str(business_detail.business_id)
        rec_detail['city'] = str(business_detail.city)
        rec_detail['state'] = str(business_detail.state)
        rec_detail['price_list'] = price_list
        rec_detail['stars_list'] = stars_list
        rec_detail['empty_stars_list'] = empty_stars_list
        context[i] = rec_detail

    print "Go to Recommendation!"
    return render(request, 'demo/recommendation.html', context)		


