from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Patient
from django.contrib.auth.decorators import permission_required

# عرض جميع المرضى
@permission_required('app.view_patient', raise_exception=True)
def get_patients(request):
    patients = Patient.objects.all()
    patients_data = [{"id": patient.id, "full_name": patient.full_name, "gender": patient.gender,
                      "date_of_birth": patient.date_of_birth, "blood_type": patient.blood_type,
                      "contact_number": patient.contact_number, "medical_condition": patient.medical_condition}
                     for patient in patients]
    return JsonResponse({"patients": patients_data})

# إضافة مريض جديد
@permission_required('app.add_patient', raise_exception=True)
def add_patient(request):
    if request.method == 'POST':
        # جمع البيانات من الـ POST request
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        blood_type = request.POST.get('blood_type')
        contact_number = request.POST.get('contact_number')
        medical_condition = request.POST.get('medical_condition')
        
        # إنشاء مريض جديد
        patient = Patient.objects.create(
            full_name=full_name,
            gender=gender,
            date_of_birth=date_of_birth,
            blood_type=blood_type,
            contact_number=contact_number,
            medical_condition=medical_condition
        )

        return JsonResponse({"message": "Patient added successfully", "patient_id": patient.id})

# تحديث بيانات مريض
@permission_required('app.change_patient', raise_exception=True)
def update_patient(request, patient_id):
    # البحث عن المريض باستخدام المعرف
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # تحديث البيانات استنادًا إلى البيانات المدخلة في الـ POST
        patient.full_name = request.POST.get('full_name', patient.full_name)
        patient.gender = request.POST.get('gender', patient.gender)
        patient.date_of_birth = request.POST.get('date_of_birth', patient.date_of_birth)
        patient.blood_type = request.POST.get('blood_type', patient.blood_type)
        patient.contact_number = request.POST.get('contact_number', patient.contact_number)
        patient.medical_condition = request.POST.get('medical_condition', patient.medical_condition)

        patient.save()
        return JsonResponse({"message": "Patient updated successfully"})

# حذف مريض
@permission_required('app.delete_patient', raise_exception=True)
def delete_patient(request, patient_id):
    # البحث عن المريض باستخدام المعرف
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return JsonResponse({"message": "Patient deleted successfully"})
