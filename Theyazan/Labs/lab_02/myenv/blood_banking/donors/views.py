# views.py
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import Donor
from .serializers import DonorSerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [AllowAny]  # السماح لجميع الطلبات بدون أذونات
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Donor
from .forms import DonorForm

# عرض قائمة المتبرعين
class DonorListView(ListView):
    model = Donor
    template_name = 'donors/donor_list.html'
    context_object_name = 'donors'

# إضافة متبرع جديد
class DonorCreateView(CreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor_list')

# تعديل بيانات متبرع
class DonorUpdateView(UpdateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_edit_form.html'
    success_url = reverse_lazy('donor_list')

# حذف متبرع
class DonorDeleteView(DeleteView):
    model = Donor
    template_name = 'donors/donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')
