from django.contrib import admin

from .models import User, Business, Rating

# Register your models here.
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Rating)