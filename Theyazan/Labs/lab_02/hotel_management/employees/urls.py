# employ/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api, name='login_api'),  # رابط API لتسجيل الدخول
    path('logout/', views.logout_api, name='logout_api'),  # رابط API لتسجيل الخروج
    path('add_employee/', views.add_employee, name='add_employee'),  # رابط لإضافة موظف
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),  # رابط لتعديل موظف
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),  # رابط لحذف موظف
]
