from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف الإشعارات
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()  # استرجاع جميع الإشعارات
    serializer_class = NotificationSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لتغيير حالة القراءة للإشعار
    @action(detail=True, methods=['put'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=200)
