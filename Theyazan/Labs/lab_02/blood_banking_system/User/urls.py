from django.urls import path ,include
from . import views

urlpatterns = [
    # روابط المستخدمين'
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('user/', views.get_users, name='get_users'),
    path('user /add/', views.add_user, name='add_user'),
    path('user /<int:user_id>/update/', views.update_user, name='update_user'),
    path('user /<int:user_id>/delete/', views.delete_user, name='delete_user'),
]