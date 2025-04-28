# patients/urls.py

from django.urls import path
from . import views

app_name = 'patients'
urlpatterns = [
    path('', views.patients_home, name='home'),  # الصفحة الرئيسية للمرضى
    path('show/', views.patients_list, name='show'),  # قائمة المرضى
    path('create/', views.patient_create, name='create'),  # إضافة مريض
    path('update/<int:pk>/', views.patient_edit, name='edit'),  # تعديل بيانات المريض
    path('delete/<int:pk>/', views.patient_delete, name='delete'),  # حذف مريض
    path('show/<int:pk>/', views.patient_show_detail, name='showdetail'),  # عرض تفاصيل المريض
    path('success/', views.success_message, name='success_message'),  # رسالة نجاح
    path('error/', views.error_page, name='error_page'),  # رسالة خطأ
    path('forms/', views.show_forms, name='forms'),  # المسار لعرض النموذج

]
