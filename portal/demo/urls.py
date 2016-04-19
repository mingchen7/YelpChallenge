from django.conf.urls import url

from . import views

app_name = 'demo'
urlpatterns = [
    url(r'^$', views.user, name = 'user'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^business/$', views.business),
    url(r'^business/(?P<page_num>[0-9]+)/$', views.business, name = 'business'),
    url(r'^detail/$', views.detail, name = 'detail'),
    url(r'^recommendation/$', views.recommendation, name = 'recommendation')
]