# blood_donation/urls.py
from django.urls import path
from . import views
from .views import DonorListView,RareBloodTypesView ,DonorCreateView, DonorUpdateView, DonorDeleteView, DonorSearchView, DonorByDateView

urlpatterns = [
    path('donors/', views.DonorListView.as_view(), name='donor-list'),
    #path('donors/create/', views.DonorCreateView.as_view(), name='donor-create'),
    path('donors/caret/', DonorCreateView.as_view(), name='donor-create'),
    path('donors/update/<int:pk>/', views.DonorUpdateView.as_view(), name='donor-update'),
    path('donors/delete/<int:pk>/', views.DonorDeleteView.as_view(), name='donor-delete'),
    path('donors/search/', views.DonorSearchView.as_view(), name='donor-search'),
    path('donors/stock/', views.DonorByDateView.as_view(), name='donor-stock'),
    path('donors/rare-blood-types/', RareBloodTypesView.as_view(), name='rare-blood-types'),

]
