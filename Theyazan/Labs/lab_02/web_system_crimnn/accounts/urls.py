from django.urls import path
from .views import CustomLogoutView  # استيراد CustomLogoutView
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

app_name = 'accounts'


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('logout/', views.CustomLogout, name='logout'),

]