

# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # روابط الإشعارات
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/add/', views.add_notification, name='add_notification'),
    path('notifications/<int:notif_id>/update/', views.update_notification, name='update_notification'),
]
