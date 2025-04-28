from django.urls import path
from . import views

urlpatterns = [
    path('court-actions/<int:pk>/', views.court_actions, name='court_actions'),
    path('', views.investigation_list, name='investigation_list'),
    path('add/<int:crime_id>/', views.add_investigation, name='add_investigation'),
    path('edit/<int:investigation_id>/', views.edit_investigation, name='edit_investigation'),
    path('delete/<int:investigation_id>/', views.delete_investigation, name='delete_investigation'),

]


