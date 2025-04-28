"""
URL configuration for blood_banking_system project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
     # إضافة روابط التطبيقات الأخرى
    path('user/', include('User.urls')),  # روابط المستخدمين
    path('donor/', include('Donors.urls')),  # روابط المتبرعين
    path('donations/', include('Donation.urls')),  # روابط التبراعات
    path('Inventory/', include('Inventory.urls')),  # روابط المخزون
    path('Laboratory/', include('Laboratory.urls')),  # روابط المختبرات
    path('Notification/', include('Notification.urls')),  # روابط الاشغارات
    path('Log/', include('Log.urls')),  # روابط السجلات
    path('Patient/', include('Patient.urls')),  # روابط المرضى
    path('Requests/', include('Requests.urls')),  # روابط الطليات
    path('User/', include('User.urls')),  # روابط المستخدمين

    # ... روابط باقي التطبيقات
]
