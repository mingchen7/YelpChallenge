from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def user(request):
	context = {
		'id': 'user'
	}
	print "in the view"
	return render(request, 'demo/user.html', context)	
