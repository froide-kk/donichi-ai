from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^talk/$', views.talk, name='talk'),
]
