from django.urls import path
from . import views

urlpatterns = [
    path('', views.BloodUnitListView.as_view(), name='blood_unit_list'),
    path('create/', views.BloodUnitCreateView.as_view(), name='blood_unit_create'),
    path('edit/<int:pk>/', views.BloodUnitUpdateView.as_view(), name='blood_unit_edit'),
    path('delete/<int:pk>/', views.BloodUnitDeleteView.as_view(), name='blood_unit_delete'),
]
