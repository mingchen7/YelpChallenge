from django.conf.urls import url

from . import views

app_name = 'demo'
urlpatterns = [
    url(r'^$', views.user, name = 'user'),
    url(r'^register/$', views.register, name = 'register'),    
    url(r'^business/(?P<page_num>[0-9]+)/(?P<cust_id>[0-9]+)/$', views.business, name = 'business'),
    url(r'^detail/(?P<restaurant_id>[0-9]+)/(?P<cust_id>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^rating/(?P<restaurant_id>[0-9]+)/(?P<cust_id>[0-9]+)/(?P<rating>[0-9])/', views.rating, name = 'rating'),
    url(r'^recommendation/(?P<cust_id>[0-9]+)/$', views.recommendation, name = 'recommendation')
]