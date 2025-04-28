from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BloodRequest
from .forms import BloodRequestForm
from blood_units.models import BloodUnit  # استيراد نموذج وحدات الدم

# عرض قائمة الطلبات
class BloodRequestListView(ListView):
    model = BloodRequest
    template_name = 'blood_requests/bloodrequest_list.html'
    context_object_name = 'blood_requests'

# إضافة طلب دم جديد
class BloodRequestCreateView(CreateView):
    model = BloodRequest
    form_class = BloodRequestForm
    template_name = 'blood_requests/bloodrequest_form.html'
    success_url = reverse_lazy('blood_request_list')

    def form_valid(self, form):
        # قبل حفظ الطلب، نقوم بالتحقق من المخزون المتاح
        blood_type = form.cleaned_data['blood_type']
        quantity_required = form.cleaned_data['quantity']

        # نحصل على جميع وحدات الدم التي تتطابق مع نوع الدم
        available_blood_units = BloodUnit.objects.filter(blood_type=blood_type)

        # حساب إجمالي الكمية المتاحة
        total_available_quantity = sum(unit.quantity for unit in available_blood_units)

        # إذا كانت الكمية المطلوبة أقل من أو تساوي المخزون المتاح
        if total_available_quantity >= quantity_required:
            # إذا كان الطلب قابلًا للتحقيق، نقوم بحفظه
            response = super().form_valid(form)
            messages.success(self.request, 'تم تقديم الطلب بنجاح.')
            return response
        else:
            # إذا لم يكن هناك مخزون كافٍ، نقوم بتحديد حالة الطلب على أنه "مرفوض"
            form.instance.status = 'rejected'
            response = super().form_valid(form)
            messages.error(self.request, 'تم رفض الطلب بسبب عدم توفر الكمية المطلوبة في المخزون.')
            return response

# تعديل بيانات طلب الدم
class BloodRequestUpdateView(UpdateView):
    model = BloodRequest
    form_class = BloodRequestForm
    template_name = 'blood_requests/bloodrequest_edit_form.html'
    success_url = reverse_lazy('blood_request_list')

    def form_valid(self, form):
        # قبل حفظ التعديلات، نقوم بالتحقق من المخزون المتاح
        blood_type = form.cleaned_data['blood_type']
        quantity_required = form.cleaned_data['quantity']

        # نحصل على جميع وحدات الدم التي تتطابق مع نوع الدم
        available_blood_units = BloodUnit.objects.filter(blood_type=blood_type)

        # حساب إجمالي الكمية المتاحة
        total_available_quantity = sum(unit.quantity for unit in available_blood_units)

        # إذا كانت الكمية المطلوبة أقل من أو تساوي المخزون المتاح
        if total_available_quantity >= quantity_required:
            # إذا كان الطلب قابلًا للتحقيق، نقوم بحفظه
            response = super().form_valid(form)
            messages.success(self.request, 'تم تحديث الطلب بنجاح.')
            return response
        else:
            # إذا لم يكن هناك مخزون كافٍ، نقوم بتحديد حالة الطلب على أنه "مرفوض"
            form.instance.status = 'rejected'
            response = super().form_valid(form)
            messages.error(self.request, 'تم رفض الطلب بسبب عدم توفر الكمية المطلوبة في المخزون.')
            return response

# حذف طلب دم
class BloodRequestDeleteView(DeleteView):
    model = BloodRequest
    template_name = 'blood_requests/bloodrequest_confirm_delete.html'
    success_url = reverse_lazy('blood_request_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'تم حذف الطلب بنجاح.')
        return super().delete(request, *args, **kwargs)