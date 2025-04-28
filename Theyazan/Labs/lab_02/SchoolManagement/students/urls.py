from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('<int:student_id>/delete/', views.student_delete, name='student_delete'),
]
