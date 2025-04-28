from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# تعريف الروتر
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/delete/', CustomerViewSet.as_view({'delete': 'destroy'}), name='customer-delete'),

]
