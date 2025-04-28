


    
   
   
   
    # روابط الطلبات
from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.get_requests, name='get_requests'),
    path('requests/add/', views.add_request, name='add_request'),
]