from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_id', 'room','number_of_rooms', 'check_in_date', 'check_out_date', 'total_amount', 'status']
    list_filter = ['status', 'check_in_date', 'check_out_date']
    search_fields = ['reservation_id', 'room__room_number']
    ordering = ['-check_in_date']
