from django.urls import path
from . import views
app_name = 'suspects'
urlpatterns = [
    path('', views.suspect_list, name='suspect_list'),  # قائمة جميع المجني عليهم
    path('list/<int:crime_id>/', views.suspect_list_for_crime, name='suspect_list_for_crime'),  # عرض المجني عليهم للجريمة
    path('add-suspect/<int:crime_id>/', views.add_suspect, name='add_suspect'),  # إضافة متهم
    path('edit-suspect/<int:suspect_id>/', views.edit_suspect, name='edit_suspect'),  # تعديل متهم
    path('search-suspects/', views.search_suspects, name='search_suspects'),
    path('delete-suspect/<int:suspect_id>/', views.delete_suspect, name='delete_suspect'),  # حذف متهم
]

