from django.urls import path
from . import views

app_name = 'Doctor'
urlpatterns = [
    path('', views.doctors_home, name='doctors_home'),  # الصفحة الرئيسية للأطباء
    path('show/', views.doctors_list, name='doctors_list'),  # قائمة الأطباء
    path('create/', views.doctor_create, name='doctor_create'),  # إضافة طبيب
    path('update/<int:pk>/', views.doctor_edit, name='doctor_edit'),  # تعديل بيانات الطبيب
    path('delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),  # حذف طبيب
    path('show/<int:pk>/', views.doctor_show_detail, name='doctor_show_detail'),  # عرض تفاصيل الطبيب
    path('success/', views.doctor_success_message, name='doctor_success_message'),  # رسالة نجاح
    path('error/', views.doctor_error_page, name='doctor_error_page'),  # رسالة خطأ
]
