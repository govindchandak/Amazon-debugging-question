from django.urls import path

from . import views

urlpatterns = [path('me/summary', views.my_summary)]
