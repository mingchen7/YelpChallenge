from django.shortcuts import render

# Create your views here.

def user(request):
	return HttpResponse("hello world!")
