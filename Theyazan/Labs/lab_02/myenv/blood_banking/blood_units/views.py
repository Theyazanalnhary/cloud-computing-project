from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BloodUnit
from .forms import BloodUnitForm  # تأكد من أنك قد قمت بإنشاء نموذج (Form) لـ BloodUnit
from .models import Donor
# عرض قائمة الوحدات الدموية
class BloodUnitListView(ListView):
    model = BloodUnit
    template_name = 'blood_units/bloodunit_list.html'
    context_object_name = 'blood_units'

# إضافة وحدة دم جديدة
class BloodUnitCreateView(CreateView):
    model = BloodUnit
    form_class = BloodUnitForm  # تأكد من أنك قد أنشأت النموذج الخاص بوحدات الدم
    template_name = 'blood_units/bloodunit_form.html'
    success_url = reverse_lazy('blood_unit_list')  # التأكد من صحة الرابط بعد إضافة الوحدة
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donors'] = Donor.objects.all()  # تمرير المتبرعين للقالب
        return context
# تعديل بيانات وحدة دم
class BloodUnitUpdateView(UpdateView):
    model = BloodUnit
    form_class = BloodUnitForm
    template_name = 'blood_units/bloodunit_edit_form.html'
    success_url = reverse_lazy('blood_unit_list')

# حذف وحدة دم
class BloodUnitDeleteView(DeleteView):
    model = BloodUnit
    template_name = 'blood_units/bloodunit_confirm_delete.html'
    success_url = reverse_lazy('blood_unit_list')
