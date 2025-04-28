from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('', views.index, name='index'),  # مسار الصفحة الرئيسية
    path('logout/', LogoutView.as_view(), name='logout'),
    path('officers/', views.officer_list, name='officer_list'),
    path('officers/create/', views.create_officer, name='create_officer'),
    path('officers/edit/<int:officer_id>/', views.edit_officer, name='edit_officer'),
    path('officers/delete/<int:officer_id>/', views.delete_officer, name='delete_officer'),
]