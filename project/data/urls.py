from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name="welcome"), # path call method from views file
    path('home.html', views.home, name="home"), # path call method from views file
    path('meteo.html', views.meteo, name="meteo"), 
    path('load_regions', views.load_regions, name='load_regions'),
    path('delete_regions', views.delete_regions, name='delete_regions'),
]
