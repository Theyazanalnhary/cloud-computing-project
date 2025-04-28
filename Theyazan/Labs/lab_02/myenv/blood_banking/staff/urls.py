from django.urls import path
from .views import (
    LoginView, logout_view, HomeView,  # استيراد HomeView بدلاً من home_view
    CreateStaffView, StaffListView, edit_staff, DeleteStaffView  # استيراد الدوال الأخرى
)
from rest_framework.views import APIView

app_name = 'staff'

urlpatterns = [
    # تسجيل الدخول والخروج
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # الصفحة الرئيسية
    path('', HomeView.as_view(), name='home'),  # استخدام HomeView للصفحة الرئيسية

    # إدارة الموظفين
    path('staff/', StaffListView.as_view(), name='staff_list'),  # عرض قائمة الموظفين
    path('staff/add/', CreateStaffView.as_view(), name='add_staff'),  # إضافة موظف جديد
    path('staff/edit/<int:staff_id>/', edit_staff, name='edit_staff'),  # تعديل موظف
    path('staff/delete/<int:staff_id>/', DeleteStaffView.as_view(), name='delete_staff'),  # حذف موظف
]