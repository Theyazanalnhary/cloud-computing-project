from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<int:room_id>/', views.room_detail, name='room_detail'),
    path('add/', views.add_room, name='add_room'),
    path('update/<int:room_id>/', views.update_room, name='update_room'),
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('search-available-rooms/', views.search_available_rooms, name='search_available_rooms'),
    path('roomes/<int:room_id>/upload_image/', views.upload_room_image, name='upload_room_image'),
]

