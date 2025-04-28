from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # رابط لوحة التحكم الخاصة بدجانغو
    path('user/', include('user.urls')),  # تضمين روابط تطبيق المستخدم
]