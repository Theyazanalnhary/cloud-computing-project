# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # روابط المخزون
    path('inventory/', views.get_inventory, name='get_inventory'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/<int:inventory_id>/update/', views.update_inventory, name='update_inventory'),
    path('inventory/<int:inventory_id>/delete/', views.delete_inventory, name='delete_inventory'),
]
