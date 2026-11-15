from django.urls import path

from applications import views as app_views

from . import views

urlpatterns = [
    path('', views.list_drives),
    path('search', views.search_drives),
    path('stats', views.drive_stats),
    path('<int:pk>', views.drive_detail),
    path('<int:drive_id>/saved', views.save_drive),
    path('<int:drive_id>/notes', views.add_note),
    path('<int:drive_id>/eligibility', views.eligibility),
    path('<int:drive_id>/close', views.close_drive),
    path('<int:drive_id>/apply', app_views.apply),
    path('<int:drive_id>/shortlist', app_views.shortlist),
    path('<int:drive_id>/shortlist/confirm', app_views.confirm_shortlist),
]
