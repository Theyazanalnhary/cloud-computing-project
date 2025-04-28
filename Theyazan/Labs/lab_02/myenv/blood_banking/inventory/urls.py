# inventory/urls.py

from django.urls import path
from . import views 
from .views import inventory_list , inventory_add 

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),  # عرض قائمة المخزون
    path('add/', views.inventory_add, name='inventory_add'),  # إضافة عنصر جديد
    path('<int:item_id>/edit/', views.inventory_edit, name='inventory_edit'),  # تعديل عنصر
    path('<int:item_id>/delete/', views.inventory_delete, name='inventory_delete'),  # حذف عنصر
]
