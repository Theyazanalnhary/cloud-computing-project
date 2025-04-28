from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='list'),
    path('create/', views.ReportCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ReportUpdateView.as_view(), name='update'),
    path('<int:pk>/add-evidence/', views.EvidenceCreateView.as_view(), name='add_evidence'),
    path('<int:pk>/add-investigation/', views.InvestigationCreateView.as_view(), name='add_investigation'),
    path('map/', views.MapView.as_view(), name='map'),
    path('search/', views.AdvancedSearchView.as_view(), name='advanced_search'),
    path('export/csv/', views.export_reports_csv, name='export_csv'),
    path('export/excel/', views.export_reports_excel, name='export_excel'),
] 