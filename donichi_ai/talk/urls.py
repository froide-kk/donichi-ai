from django.conf.urls import url
from talk import views

urlpatterns = [
    url(r'', views.index, name='index'),
]
