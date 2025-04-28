from django.contrib import admin
from .models import Agent, Bill, Booking, Country, Detail, DocType, Guestbook, Guest, PaymentMode, Rate, Reservation, Room, RoomType, Transaction, User, Session, TransactionType, UsersOnline, Payment

# Registering the models
admin.site.register(Agent)
admin.site.register(Bill)
admin.site.register(Booking)
admin.site.register(Country)
admin.site.register(Detail)
admin.site.register(DocType)
admin.site.register(Guestbook)
admin.site.register(Guest)
admin.site.register(PaymentMode)
admin.site.register(Rate)
admin.site.register(Reservation)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Transaction)
admin.site.register(User)
admin.site.register(Session)
admin.site.register(TransactionType)
admin.site.register(UsersOnline)
admin.site.register(Payment)
