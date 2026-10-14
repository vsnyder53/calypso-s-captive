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
urlpatterns=[
    path('home/', views.teacher_page, name="home"), 
    path("admin/", admin.site.urls),                 
    path('login/', views.login_page, name='login_page'),    
    path('register/', views.register_page, name='register'),
    path('my-students/', views.my_students_view, name='my_students'),
    path('guardian/', views.guardian_page, name='guardian'),
    path('all-students/', views.all_students_view, name='all_students'),
    path('student_scan/', views.student_scan, name='student_scan'),
    path('add-student/', views.add_student_view, name='add_student'),
    path('add-guardian/', views.add_guardian_view, name='add_guardian'),
    path('add-payment/', views.add_payment_view, name='add_payment'),
    path('student_scan/', views.student_scan, name='add_student_scan'),
    path('student/profile/<str:student_id>/', views.student_profile_view, name='student_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += staticfiles_urlpatterns()