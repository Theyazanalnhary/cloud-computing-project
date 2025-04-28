from django.urls import path
from . import views

urlpatterns = [
    path('', views.prosecution_list, name='prosecution_list'),
    path('add/<int:crime_id>/', views.add_prosecution, name='add_prosecution'),
    path('edit/<int:prosecution_id>/', views.edit_prosecution, name='edit_prosecution'),
    path('delete/<int:prosecution_id>/', views.delete_prosecution, name='delete_prosecution'),
]
