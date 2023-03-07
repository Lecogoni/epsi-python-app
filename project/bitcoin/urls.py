from django.urls import path, include
from . import views

urlpatterns = [
    path('bitcoin', views.display_chart, name="getbitcoin"),
]