from django.urls import include, path

urlpatterns = [
    path("", include("helpdesk.urls")),
]
