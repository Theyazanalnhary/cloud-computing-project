"""
URL configuration for hotel_management project.

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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

       # روابط التطبيقات الخاصة بك:
    path('api/', include('customers.urls')),  # API للعملاء
    path('api/roomes/', include('Roomes.urls')),  # API للغرف
    path('api/reviews/', include('reviews.urls')),  # API للتقييمات
    path('api/reservations/', include('reservations.urls')),  # API للحجوزات
    path('api/payments/', include('payments.urls')),  # API للمدفوعات
    path('api/offers/', include('offers.urls')),  # API للعروض
    path('api/notifications/', include('notifications.urls')),  # API للإشعارات
    path('api/services/', include('services.urls')),  # API للخدمات
    path('api/reports/', include('reports.urls')),  # API للتقارير
    path('api/employees/',include('employees.urls')),
    path('api/logs/',include('logs.urls')),
    path('api/inventory/',include('inventory.urls')),
    path('api/Users/', include('Users.urls')),
]

 #إضافة إعدادات للوصول إلى الصور في الوضع المحلي
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)