from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), # path call method from views file
    path('about.html', views.about, name="about"), 
    path('load_regions', views.load_regions, name='load_regions'),
    path('delete_regions', views.delete_regions, name='delete_regions'),
]
