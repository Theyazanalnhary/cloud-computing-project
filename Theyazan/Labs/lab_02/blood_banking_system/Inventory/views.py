from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
from .models import Inventory, Donation

# عرض جميع المخزونات
@permission_required('app.view_inventory', raise_exception=True)
def get_inventory(request):
    inventory_items = Inventory.objects.all()
    inventory_data = [{"id": item.id, "blood_type": item.blood_type, "quantity_in_ml": item.quantity_in_ml, "status": item.status} for item in inventory_items]
    return JsonResponse({"inventory": inventory_data})

# إضافة مخزون
@permission_required('app.add_inventory', raise_exception=True)
def add_inventory(request):
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        quantity_in_ml = request.POST.get('quantity_in_ml')
        status = request.POST.get('status')
        expiry_date = request.POST.get('expiry_date')

        # إضافة عنصر مخزون جديد
        inventory_item = Inventory.objects.create(
            blood_type=blood_type,
            quantity_in_ml=quantity_in_ml,
            status=status,
            expiry_date=expiry_date
        )

        return JsonResponse({"message": "Inventory item added successfully", "inventory_id": inventory_item.id})

# تحديث المخزون
@permission_required('app.change_inventory', raise_exception=True)
def update_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory_item.quantity_in_ml = request.POST.get('quantity_in_ml', inventory_item.quantity_in_ml)
        inventory_item.status = request.POST.get('status', inventory_item.status)
        inventory_item.expiry_date = request.POST.get('expiry_date', inventory_item.expiry_date)
        inventory_item.save()
        return JsonResponse({"message": "Inventory item updated successfully"})

# حذف عنصر من المخزون
@permission_required('app.delete_inventory', raise_exception=True)
def delete_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    inventory_item.delete()
    return JsonResponse({"message": "Inventory item deleted successfully"})
