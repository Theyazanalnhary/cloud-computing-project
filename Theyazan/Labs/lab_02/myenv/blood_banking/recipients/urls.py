# recipients/urls.py

from django.urls import path
from .views import RecipientListCreate, RecipientDetail

urlpatterns = [
    path('recipients/', RecipientListCreate.as_view(), name='recipient-list'),
    path('recipients/<int:pk>/', RecipientDetail.as_view(), name='recipient-detail'),
]
