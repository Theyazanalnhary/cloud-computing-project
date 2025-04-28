from django.urls import path
from .views import crime_list, crime_detail, crime_create, crime_update, crime_delete,crime_full_report

urlpatterns = [
    path('', crime_list, name='crime_list'),              # عرض الجرائم مع البحث
    path('crime/<int:pk>/', crime_detail, name='crime_detail'),  # تفاصيل جريمة
    path('crime/new/', crime_create, name='crime_create'),       # إضافة جريمة
    path('crime/<int:pk>/edit/', crime_update, name='crime_update'), # تعديل جريمة
    path('crime/<int:pk>/delete/', crime_delete, name='crime_delete'), # حذف جريمة
    path('crime-report/<int:crime_id>/', crime_full_report, name='crime_full_report'),

]