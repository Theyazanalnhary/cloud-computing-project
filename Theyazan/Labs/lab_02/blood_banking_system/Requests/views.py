from .models import Request
from django.contrib.auth.decorators import permission_required

# عرض جميع الطلبات
@permission_required('app.view_request', raise_exception=True)
def get_requests(request):
    requests = Request.objects.all()
    requests_data = [{"id": req.id, "blood_type": req.blood_type, "quantity_in_ml": req.quantity_in_ml} for req in requests]
    return JsonResponse({"requests": requests_data})

# إضافة طلب
@permission_required('app.add_request', raise_exception=True)
def add_request(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        blood_type = request.POST.get('blood_type')
        quantity_in_ml = request.POST.get('quantity_in_ml')
        status = request.POST.get('status')

        patient = get_object_or_404(Patient, id=patient_id)

        # إضافة الطلب
        req = Request.objects.create(
            patient=patient, blood_type=blood_type, quantity_in_ml=quantity_in_ml, status=status
        )

        return JsonResponse({"message": "Request added successfully", "request_id": req.id})
