from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    # تضمين حقل الصورة بدلاً من الرابط
    room_image = serializers.ImageField(required=False)

    class Meta:
        model = Room
        fields = ['room_id', 'room_number', 'room_type', 'number_of_rooms', 'price_per_night', 'status', 'capacity', 'description', 'room_image']  # تعديل الحقل ليكون room_image بدلاً من room_image_url
