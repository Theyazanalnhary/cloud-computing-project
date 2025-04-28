# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet

# إعداد Router للـ API
router = DefaultRouter()
router.register(r'services', ServiceViewSet)  # تسجيل ServiceViewSet

urlpatterns = [
    path('api/', include(router.urls)),  # تضمين الـ URLs الخاصة بـ API
]
