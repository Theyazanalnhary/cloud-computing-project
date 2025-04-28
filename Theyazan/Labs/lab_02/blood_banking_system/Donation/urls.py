from django.urls import path
from .import views

urlpatterns = [
 # روابط التبرعات
    path('donations/add/', views.add_donation, name='add_donation'),
]