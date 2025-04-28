# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),  # عرض جميع المستخدمين
    path('users/<int:userid>/', views.user_detail, name='user_detail'),  # عرض تفاصيل مستخدم معين
    path('api/users/', views.user_list_api, name='user_list_api'),  # API لعرض جميع المستخدمين
    path('api/users/<int:userid>/', views.user_detail_api, name='user_detail_api'),  # API لعرض تفاصيل مستخدم معين
    path('api/users/add/', views.add_user, name='add_user'),  # API لإضافة مستخدم جديد
    path('api/users/update/<int:userid>/', views.update_user, name='update_user'),  # API لتعديل مستخدم
    path('api/users/delete/<int:userid>/', views.delete_user, name='delete_user'),  # API لحذف مستخدم
    path('api/users/login/', views.login_user, name='login_user'),  # API لتسجيل الدخول
]
