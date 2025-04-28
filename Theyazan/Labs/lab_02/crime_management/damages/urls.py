from django.urls import path
from . import views

urlpatterns = [
    path('', views.damage_list, name='damage_list'),
    path('add/<int:crime_id>/', views.add_damage, name='add_damage'),
    path('edit/<int:damage_id>/', views.edit_damage, name='edit_damage'),
    path('delete/<int:damage_id>/', views.delete_damage, name='delete_damage'),
]
