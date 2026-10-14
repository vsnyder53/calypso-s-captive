"""
URL configuration for captive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from capapp.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from capapp import views

# Define URL patterns
urlpatterns = [
    path('home/', views.home_page, name="home"), 
    path('home/list/', views.home_page, name="StudenList"),               
    path("admin/", admin.site.urls),                 
    path('login/', login_page, name='login_page'),    
    path('register/', register_page, name='register'),
    path('student_list/', teacher_page, name='Teacher'),
    path('guardian', guardian_page, name='guardian'),
    path('student_scan', student_scan, name='student_scan'),
    path('student_list', student_list, name='student_list'),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += staticfiles_urlpatterns()