"""
URL configuration for blood_banking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import routers
from staff.views import LoginView  # استيراد صفحة تسجيل الدخول

router = routers.DefaultRouter()
urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # عرض صفحة تسجيل الدخول عند فتح الموقع لأول مرة

    path('admin/', admin.site.urls),
    path('api/', include('donors.urls')),
    path('api/', include('blood_units.urls')),
    path('api/', include('blood_tests.urls')),
    path('api/',include('blood_requests.urls')),
    path('api/', include('recipients.urls')),
    path('api/', include('operations.urls')),
    path('api/', include('staff.urls')),
    path('api/', include('inventory.urls')),
]
