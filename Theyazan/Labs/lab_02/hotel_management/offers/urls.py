# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet

# إعداد Router لـ API
router = DefaultRouter()
router.register(r'offers', OfferViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # تضمين الـ URLs الخاصة بـ API
]
