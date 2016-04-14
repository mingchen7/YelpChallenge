from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def user(request):
	context = {
		'id': 'user'
	}	
	return render(request, 'demo/user.html', context)	

def businesses(request):
	context = {'id': 'business'}
	return render(request, 'demo/businesses.html', context)

def detail(request):
	context = {}
	return render(request, 'demo/detail.html', context)
