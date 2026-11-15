from django.urls import path

from . import views

urlpatterns = [
    path('me', views.my_applications),
    path('<int:application_id>', views.application_detail),
    path('<int:application_id>/withdraw', views.withdraw),
]
