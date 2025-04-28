# urls.py

from django.urls import path
from . import views


urlpatterns = [
    # روابط المختبرات
    path('laboratories/', views.get_laboratories, name='get_laboratories'),
    path('laboratories/add/', views.add_laboratory, name='add_laboratory'),
    path('laboratories/<int:lab_id>/update/', views.update_laboratory, name='update_laboratory'),
    path('laboratories/<int:lab_id>/delete/', views.delete_laboratory, name='delete_laboratory'),
]
