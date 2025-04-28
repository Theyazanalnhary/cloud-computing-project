from django.urls import path
from .views import DonorListView, DonorCreateView, DonorUpdateView, DonorDeleteView

urlpatterns = [
    path('donors/', DonorListView.as_view(), name='donor_list'),  # عرض المتبرعين
    path('donors/add/', DonorCreateView.as_view(), name='donor_add'),  # إضافة متبرع جديد
    path('donors/edit/<int:pk>/', DonorUpdateView.as_view(), name='donor_edit'),  # تعديل المتبرع
    path('donors/delete/<int:pk>/', DonorDeleteView.as_view(), name='donor_delete'),  # حذف المتبرع
]
