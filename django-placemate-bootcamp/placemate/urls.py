from django.urls import include, path

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/students/', include('accounts.student_urls')),
    path('api/drives/', include('drives.urls')),
    path('api/applications/', include('applications.urls')),
]
