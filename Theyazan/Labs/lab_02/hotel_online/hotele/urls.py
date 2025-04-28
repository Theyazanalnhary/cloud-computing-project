from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import LoginAPIView
# Set up the router and register the viewsets
router = DefaultRouter()
router.register(r'agents', views.AgentViewSet)
router.register(r'bills', views.BillViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'details', views.DetailViewSet)
router.register(r'doctypes', views.DocTypeViewSet)
router.register(r'guestbooks', views.GuestbookViewSet)
router.register(r'guests', views.GuestViewSet)
router.register(r'paymentmodes', views.PaymentModeViewSet)
router.register(r'rates', views.RateViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'roomtypes', views.RoomTypeViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'transactiontypes', views.TransactionTypeViewSet)
router.register(r'usersonline', views.UsersOnlineViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login')
]
