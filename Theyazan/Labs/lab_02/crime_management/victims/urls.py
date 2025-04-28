from django.urls import path
from . import views

urlpatterns = [
    path('', views.victim_list, name='victim_list'),  # قائمة جميع المجني عليهم
    path('add/<int:crime_id>/', views.add_victim_for_crime, name='add_victim_for_crime'),  # إضافة مجني عليه
    path('list/<int:crime_id>/', views.victim_list_for_crime, name='victim_list_for_crime'),  # عرض المجني عليهم للجريمة
    path('edit/<int:victim_id>/', views.edit_victim, name='edit_victim'),  # تعديل مجني عليه
    path('delete/<int:victim_id>/', views.delete_victim, name='delete_victim'),  # حذف مجني عليه
]