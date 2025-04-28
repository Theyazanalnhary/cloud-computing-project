# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # عرض جميع المرضى
    path('patients/', views.get_patients, name='get_patients'),
    
    # إضافة مريض جديد
    path('patients/add/', views.add_patient, name='add_patient'),
    
    # تحديث بيانات مريض
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),
    
    # حذف مريض
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]
