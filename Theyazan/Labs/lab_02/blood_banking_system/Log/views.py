from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
from .models import Log

# عرض سجلات الأنشطة
@permission_required('app.view_log', raise_exception=True)
def get_logs(request):
    logs = Log.objects.all()
    logs_data = [{"id": log.id, "action": log.action, "timestamp": log.timestamp} for log in logs]
    return JsonResponse({"logs": logs_data})

# إضافة سجل
@permission_required('app.add_log', raise_exception=True)
def add_log(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user  # الحصول على المستخدم الحالي

        # إضافة سجل نشاط جديد
        log = Log.objects.create(user=user, action=action)

        return JsonResponse({"message": "Log added successfully", "log_id": log.id})
