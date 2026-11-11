from django.urls import path

from . import views

urlpatterns = [
    path("api/tickets", views.tickets),
    path("api/tickets/<int:ticket_id>", views.ticket_detail),
    path("api/tickets/<int:ticket_id>/reply", views.replies),
    path("api/tickets/<int:ticket_id>/status", views.ticket_status),
    path("api/notifications/count", views.notification_count),
]
