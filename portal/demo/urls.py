from django.conf.urls import url

from . import views

# app_name = 'demo'
urlpatterns = [
    url(r'^$', views.user, name='user'),
]