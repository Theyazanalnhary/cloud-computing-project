from rest_framework import viewsets
from .models import Agent, Bill, Booking, Country, Detail, DocType, Guestbook, Guest, PaymentMode, Rate, Reservation, Room, RoomType, Transaction, User, Session, TransactionType, UsersOnline, Payment
from .serializers import AgentSerializer, BillSerializer, BookingSerializer, CountrySerializer, DetailSerializer, DocTypeSerializer, GuestbookSerializer, GuestSerializer, PaymentModeSerializer, RateSerializer, ReservationSerializer, RoomSerializer, RoomTypeSerializer, TransactionSerializer, UserSerializer, SessionSerializer, TransactionTypeSerializer, UsersOnlineSerializer, PaymentSerializer
 
# Create viewsets for each model
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer

class DocTypeViewSet(viewsets.ModelViewSet):
    queryset = DocType.objects.all()
    serializer_class = DocTypeSerializer

class GuestbookViewSet(viewsets.ModelViewSet):
    queryset = Guestbook.objects.all()
    serializer_class = GuestbookSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class PaymentModeViewSet(viewsets.ModelViewSet):
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer

@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # حفظ البيانات في قاعدة البيانات
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User

class LoginAPIView(APIView):
    def post(self, request):
        # استقبال البيانات
        loginname = request.data.get("loginname")
        password = request.data.get("password")

        # التحقق من البيانات المدخلة
        if not loginname or not password:
            return Response({"error": "يجب إدخال اسم المستخدم وكلمة المرور"}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق من وجود المستخدم
        try:
            user = User.objects.get(loginname=loginname)
        except User.DoesNotExist:
            return Response({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}, status=status.HTTP_401_UNAUTHORIZED)

        # التحقق من كلمة المرور
        if check_password(password, user.password):
            return Response({"message": "تم تسجيل الدخول بنجاح"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}, status=status.HTTP_401_UNAUTHORIZED)

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer

class UsersOnlineViewSet(viewsets.ModelViewSet):
    queryset = UsersOnline.objects.all()
    serializer_class = UsersOnlineSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
