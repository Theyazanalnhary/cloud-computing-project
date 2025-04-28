from django.urls import path
from .views import OperationListCreate, OperationDetail

urlpatterns = [
    path('operations/', OperationListCreate.as_view(), name='operation-list'),
    path('operations/<int:pk>/', OperationDetail.as_view(), name='operation-detail'),
]
