from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def room_detail(request, room_id):
    # استخدام get_object_or_404 لتحميل الغرفة أو إرجاع 404 إذا لم توجد
    room = get_object_or_404(Room, room_id=room_id)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['POST'])
def add_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_room(request, room_id):
    # استخدام get_object_or_404 لتحميل الغرفة أو إرجاع 404 إذا لم توجد
    room = get_object_or_404(Room, room_id=room_id)
    serializer = RoomSerializer(room, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_room(request, room_id):
    # استخدام get_object_or_404 لتحميل الغرفة أو إرجاع 404 إذا لم توجد
    room = get_object_or_404(Room, room_id=room_id)
    room.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def upload_room_image(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # التحقق من وجود صورة في الملفات المرسلة
    if 'room_image' in request.FILES:
        # التحقق من نوع الصورة (مثلاً فقط jpg أو png)
        room_image = request.FILES['room_image']
        if room_image.content_type not in ['image/jpeg', 'image/png']:
            return Response({'error': 'الملف يجب أن يكون صورة بصيغة JPEG أو PNG'},
                            status=status.HTTP_400_BAD_REQUEST)

        # تخزين الصورة في حقل room_image
        room.room_image = room_image
        room.save()

        # إرجاع البيانات المحدثة للغرفة
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)
# views.py
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime

# الدالة للبحث عن الغرف المتاحة
def available_rooms(check_in_date, check_out_date):
    check_in_datetime = datetime.combine(check_in_date, datetime.min.time())
    check_out_datetime = datetime.combine(check_out_date, datetime.max.time())

    available_rooms = Room.objects.filter(
        Q(status='available') &
        ~Q(reservations__check_in_date__lt=check_out_datetime,
           reservations__check_out_date__gt=check_in_datetime)
    ).distinct()

    return available_rooms


def search_available_rooms(request):
    check_in_date_str = request.GET.get('check_in_date')
    check_out_date_str = request.GET.get('check_out_date')

    try:
        if check_in_date_str and check_out_date_str:
            check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

            # التأكد من أن تاريخ الوصول قبل تاريخ المغادرة
            if check_in_date >= check_out_date:
                return JsonResponse({'error': 'تاريخ الوصول يجب أن يكون قبل تاريخ المغادرة'}, status=400)

            rooms = available_rooms(check_in_date, check_out_date)
            room_list = list(rooms.values('room_number', 'room_type', 'price_per_night', 'capacity'))
            return JsonResponse({'available_rooms': room_list}, status=200)
        else:
            return JsonResponse({'error': 'يرجى توفير تواريخ الوصول والمغادرة'}, status=400)

    except ValueError:
        return JsonResponse({'error': 'تنسيق التواريخ غير صحيح. استخدم yyyy-mm-dd'}, status=400)
