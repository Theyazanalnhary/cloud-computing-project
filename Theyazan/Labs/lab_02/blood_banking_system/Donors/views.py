from .models import Donor
from django.contrib.auth.decorators import permission_required

# عرض جميع المتبرعين
@permission_required('app.view_donor', raise_exception=True)
def get_donors(request):
    donors = Donor.objects.all()
    donors_data = [{"id": donor.id, "full_name": donor.full_name, "blood_type": donor.blood_type} for donor in donors]
    return JsonResponse({"donors": donors_data})

# إضافة متبرع
@permission_required('app.add_donor', raise_exception=True)
def add_donor(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        blood_type = request.POST.get('blood_type')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # إضافة المتبرع
        donor = Donor.objects.create(
            full_name=full_name, gender=gender, date_of_birth=date_of_birth,
            blood_type=blood_type, contact_number=contact_number, email=email, address=address
        )

        return JsonResponse({"message": "Donor added successfully", "donor_id": donor.id})

# تعديل متبرع
@permission_required('app.change_donor', raise_exception=True)
def update_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == 'POST':
        donor.full_name = request.POST.get('full_name', donor.full_name)
        donor.blood_type = request.POST.get('blood_type', donor.blood_type)
        donor.contact_number = request.POST.get('contact_number', donor.contact_number)
        donor.email = request.POST.get('email', donor.email)
        donor.address = request.POST.get('address', donor.address)
        donor.save()
        return JsonResponse({"message": "Donor updated successfully"})

# حذف متبرع
@permission_required('app.delete_donor', raise_exception=True)
def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    donor.delete()
    return JsonResponse({"message": "Donor deleted successfully"})
