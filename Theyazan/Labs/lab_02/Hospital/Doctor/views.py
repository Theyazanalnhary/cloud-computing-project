from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor
from .forms import DoctorForm
from django.urls import reverse
import os

# الصفحة الرئيسية للأطباء
def doctors_home(request):
    return render(request, 'doctors_home.html')

# عرض قائمة الأطباء
def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})

# إضافة طبيب جديد
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('Doctor:doctor_success_message'))
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})

# تعديل بيانات الطبيب
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect(reverse('Doctor:doctor_success_message'))
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_update.html', {'form': form, 'doctor': doctor})

# حذف طبيب
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if doctor.image:
        os.remove(doctor.image.path)
    if doctor.file_report:
        os.remove(doctor.file_report.path)
    doctor.delete()
    return redirect(reverse("Doctor:doctor_success_message"))

# عرض تفاصيل الطبيب
def doctor_show_detail(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    return render(request, 'doctor_info.html', {'doctor': doctor})

# صفحة تعرض رسالة نجاح
def doctor_success_message(request):
    return render(request, 'ssuccess_message.html')

# صفحة تعرض رسالة خطأ
def doctor_error_page(request):
    return render(request, 'error_page.html')
