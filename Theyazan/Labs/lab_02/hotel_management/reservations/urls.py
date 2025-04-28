from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservation-list'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('create/', views.ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation-update'),
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation-delete'),
]
