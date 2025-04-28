

from django.urls import path
from . import views

urlpatterns = [
 # روابط المتبرعين
    path('donors/', views.get_donors, name='get_donors'),
    path('donors/add/', views.add_donor, name='add_donor'),
    path('donors/<int:donor_id>/update/', views.update_donor, name='update_donor'),
    path('donors/<int:donor_id>/delete/', views.delete_donor, name='delete_donor'),
]