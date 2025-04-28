# blood_tests/admin.py
from django.contrib import admin
from .models import User, BloodTest, Recipient, BloodRequest, Operation, Inventory

admin.site.register(User)
admin.site.register(BloodTest)
admin.site.register(Recipient)
admin.site.register(BloodRequest)
admin.site.register(Operation)
admin.site.register(Inventory)
