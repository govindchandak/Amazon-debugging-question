from django.urls import path

from . import views

urlpatterns = [
    path("api/products/", views.list_products),
    path("api/wishlist/<str:customer>/", views.get_wishlist),
    path("api/wishlist/<str:customer>/items/", views.add_to_wishlist),
    path("wishlist/<str:customer>/", views.wishlist_page),
]
