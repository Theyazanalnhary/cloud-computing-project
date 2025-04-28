from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),
    path('<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),
]
