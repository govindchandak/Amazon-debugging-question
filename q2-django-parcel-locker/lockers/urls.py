from django.urls import path

from . import views

urlpatterns = [
    path("api/parcels/deposit/", views.deposit_parcel),
    path("api/parcels/pickup/", views.pickup_parcel),
    path("api/lockers/free/", views.free_lockers),
]
