
# blood_tests/urls.py

from django.urls import path
from .views import BloodTestListCreate, BloodTestDetail

urlpatterns = [
    path('tests/', BloodTestListCreate.as_view(), name='blood-test-list'),
    path('tests/<int:pk>/', BloodTestDetail.as_view(), name='blood-test-detail'),
]
