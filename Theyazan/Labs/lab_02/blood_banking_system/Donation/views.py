from Donation.models import Donation
from Inventory.models import Inventory
from django.contrib.auth.decorators import permission_required

# إضافة تبرع
@permission_required('app.add_donation', raise_exception=True)
def add_donation(request):
    if request.method == 'POST':
        donor_id = request.POST.get('donor')
        blood_type = request.POST.get('blood_type')
        volume_in_ml = request.POST.get('volume_in_ml')
        status = request.POST.get('status')
        donation_date = request.POST.get('donation_date')

        donor = get_object_or_404(Donor, id=donor_id)

        # إنشاء التبرع
        donation = Donation.objects.create(
            donor=donor, blood_type=blood_type, volume_in_ml=volume_in_ml, 
            status=status, donation_date=donation_date
        )

        # تحديث المخزون بناءً على فصيلة الدم
        inventory_item = Inventory.objects.filter(blood_type=blood_type, status='Available').first()
        if inventory_item:
            inventory_item.quantity_in_ml += volume_in_ml  # إضافة الكمية للمخزون
            inventory_item.save()

        return JsonResponse({"message": "Donation added successfully", "donation_id": donation.id})
