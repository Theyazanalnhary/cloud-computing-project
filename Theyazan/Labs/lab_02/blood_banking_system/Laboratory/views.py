from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
from Laboratory.models import Laboratory

# عرض جميع المختبرات
@permission_required('app.view_laboratory', raise_exception=True)
def get_laboratories(request):
    labs = Laboratory.objects.all()
    lab_data = [{"id": lab.id, "name": lab.name, "location": lab.location, "contact_number": lab.contact_number} for lab in labs]
    return JsonResponse({"laboratories": lab_data})

# إضافة مختبر
@permission_required('app.add_laboratory', raise_exception=True)
def add_laboratory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        contact_number = request.POST.get('contact_number')

        # إضافة مختبر جديد
        lab = Laboratory.objects.create(name=name, location=location, contact_number=contact_number)

        return JsonResponse({"message": "Laboratory added successfully", "laboratory_id": lab.id})

# تحديث مختبر
@permission_required('app.change_laboratory', raise_exception=True)
def update_laboratory(request, lab_id):
    lab = get_object_or_404(Laboratory, id=lab_id)
    if request.method == 'POST':
        lab.name = request.POST.get('name', lab.name)
        lab.location = request.POST.get('location', lab.location)
        lab.contact_number = request.POST.get('contact_number', lab.contact_number)
        lab.save()
        return JsonResponse({"message": "Laboratory updated successfully"})

# حذف مختبر
@permission_required('app.delete_laboratory', raise_exception=True)
def delete_laboratory(request, lab_id):
    lab = get_object_or_404(Laboratory, id=lab_id)
    lab.delete()
    return JsonResponse({"message": "Laboratory deleted successfully"})
