# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from .forms import InventoryItemForm  # استيراد النموذج

# Views for HTML interface
def inventory_list(request):
    """
    عرض قائمة المخزون.
    """
    items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})

def inventory_add(request):
    """
    إضافة عنصر جديد إلى المخزون.
    """
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)  # استخدام النموذج هنا
        if form.is_valid():  # التحقق من صحة البيانات المدخلة
            form.save()  # حفظ العنصر الجديد
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm()

    return render(request, 'inventory/inventory_add.html', {'form': form})

def inventory_edit(request, item_id):
    """
    تعديل عنصر موجود في المخزون.
    """
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)  # تمرير العنصر لتعديله
        if form.is_valid():  # التحقق من صحة البيانات المدخلة
            form.save()  # حفظ التعديلات
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm(instance=item)

    return render(request, 'inventory/inventory_edit.html', {'form': form, 'item': item})

def inventory_delete(request, item_id):
    """
    حذف عنصر من المخزون.
    """
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('inventory:inventory_list')

    return render(request, 'inventory/inventory_delete.html', {'item': item})
