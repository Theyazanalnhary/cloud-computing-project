from django.urls import path
from .views import BloodRequestListView, BloodRequestCreateView, BloodRequestUpdateView, BloodRequestDeleteView

urlpatterns = [
    path('blood-requests/', BloodRequestListView.as_view(), name='blood_request_list'),
    path('creat/', BloodRequestCreateView.as_view(), name='blood_request_creat'),
    path('<int:pk>/update/', BloodRequestUpdateView.as_view(), name='blood_request_update'),
    path('<int:pk>/delete/', BloodRequestDeleteView.as_view(), name='blood_request_delete'),
]
