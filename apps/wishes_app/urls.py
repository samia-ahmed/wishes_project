from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_page/$', views.add_page),
    url(r'^add_item/$', views.add_item),
    url(r'^display/(?P<wish_id>\d+)$', views.display),
    url(r'^join/(?P<wish_id>\d+)$', views.join),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
]
