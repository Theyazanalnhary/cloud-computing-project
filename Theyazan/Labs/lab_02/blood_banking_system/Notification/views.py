from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
from .models import Notification

# عرض جميع إشعارات المستخدم
@permission_required('app.view_notification', raise_exception=True)
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications_data = [{"id": notif.id, "message": notif.message, "is_read": notif.is_read} for notif in notifications]
    return JsonResponse({"notifications": notifications_data})

# إضافة إشعار
@permission_required('app.add_notification', raise_exception=True)
def add_notification(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        message = request.POST.get('message')
        recipient = get_object_or_404(User, id=recipient_id)

        # إضافة إشعار جديد
        notif = Notification.objects.create(recipient=recipient, message=message)

        return JsonResponse({"message": "Notification added successfully", "notification_id": notif.id})

# تحديث حالة القراءة
@permission_required('app.change_notification', raise_exception=True)
def update_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)
    if request.method == 'POST':
        notif.is_read = request.POST.get('is_read', notif.is_read)
        notif.save()
        return JsonResponse({"message": "Notification status updated successfully"})
