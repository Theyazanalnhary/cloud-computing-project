# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet

# إعداد Router لـ API
router = DefaultRouter()
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # تضمين الـ URLs الخاصة بـ API
]
