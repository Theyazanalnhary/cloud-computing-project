from . import views
from django.urls import path

# urls.py

urlpatterns = [
    # روابط السجلات
    path('logs/', views.get_logs, name='get_logs'),
    path('logs/add/', views.add_log, name='add_log'),
]
