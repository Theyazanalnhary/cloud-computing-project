# patients/views.py

from django.shortcuts import render
from .models import Patients
from .forms import PatientsForm
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django_filters import fields

from user.decorators import isadmin
# الصفحة الرئيسية للمرضى
def patients_home(request):
    return render(request, 'patients_home.html')

# عرض قائمة المرضى
def patients_list(request):
    patients=Patients.objects.all()  # جلب جميع المرضى من قاعدة البيانات
    if patients.exists:
       return render(request, 'patients_list.html', {'patients': patients})
    else:
        return redirect(reverse('patients_error_page'))

# إضافة مريض جديد


@isadmin
def patient_create(request):
    if request.method == 'POST':
        try:
            patient=Patients.objects.create(
                first_name=request.POST.get('fname'),
                last_name=request.POST.get('lname'),
                age=request.POST.get('age'),
                report=request.POST.get('report'),
                image=request.FILES.get('image'),
                file_report=request.FILES.get('medicalreport')

            )
            return redirect(reverse('patients:success_message'))  # الانتقال إلى صفحة النجاح بعد الإضافة
        except IntegrityError:
            return redirect(reverse('patients:error_page'))  # الانتقال إلى صفحة الخطأ إذا لم يتم التحقق من صحة النموذج
    else:
        return render(request, 'add_patient.html')


#نموذج الفورم الدلة الحاصة به

from django.shortcuts import render, redirect
from .forms import PatientsForm
from .models import Patients
from django.urls import reverse
def show_forms(request):
    if request.method == 'POST':
        form = PatientsForm(request.POST, request.FILES)
        if form.is_valid():
            # الحصول على البيانات من النموذج
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            report = form.cleaned_data['report']
            image = form.cleaned_data.get('image', None)  # image is optional
            file_report = form.cleaned_data.get('file_report', None)  # file_report is optional
            
            # حفظ البيانات في قاعدة البيانات
            patient = Patients.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                report=report,
                image=image,
                file_report=file_report
            )

            # إعادة التوجيه إلى صفحة النجاح
            return redirect(reverse('patients:success_message'))
        else:
            return HttpResponse('Form is not valid!')
    else:
        form = PatientsForm()
    return render(request, 'other_type_forms.html', {'form': form})





# تعديل بيانات المريض
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Patients

def patient_edit(request, pk):
    patient = get_object_or_404(Patients, id=pk)  # جلب المريض بناءً على معرفه
    if request.method == 'POST':
        try:
            # التحقق من القيم المدخلة
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            age = request.POST.get('age')
            report = request.POST.get('report')
            
            # تحديث الحقول التي تم إرسالها
            patient.first_name = first_name
            patient.last_name = last_name
            patient.age = age
            patient.report = report

            # إذا تم تحميل صورة جديدة
            if request.FILES.get('image'):
                patient.image = request.FILES.get('image')
            
            # إذا تم تحميل تقرير طبي جديد
            if request.FILES.get('medicalreport'):
                patient.file_report = request.FILES.get('medicalreport')
            
            # حفظ البيانات
            patient.save()

            # إعادة التوجيه إلى صفحة النجاح بعد التعديل
            return redirect(reverse("patients:success_message"))
        
        except Exception as e:
            # في حالة حدوث أي خطأ، تسجيل الخطأ وطباعة التفاصيل
            print(f"Error occurred while updating patient: {str(e)}")
            return redirect(reverse("patients:error_page"))
    
    else:
        # إذا كان الطلب GET، عرض النموذج مع بيانات المريض
        return render(request, 'patients_update.html', {'patient': patient})

 
# حذف مريض
import os
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseServerError
from .models import Patients

def patient_delete(request, pk):
    try:
        # الحصول على المريض من قاعدة البيانات
        patient = get_object_or_404(Patients, pk=pk)

        # حذف الصورة إذا كانت موجودة
        if patient.image:
            image_path = patient.image.path  # الحصول على المسار الفعلي للصورة
            if os.path.isfile(image_path):
                os.remove(image_path)

        # حذف التقرير الطبي إذا كان موجودًا
        if patient.file_report:
            file_report_path = patient.file_report.path  # الحصول على المسار الفعلي للتقرير الطبي
            if os.path.isfile(file_report_path):
                os.remove(file_report_path)

        # حذف المريض من قاعدة البيانات
        patient.delete()

        # بعد الحذف بنجاح، إعادة التوجيه إلى صفحة النجاح
        return redirect(reverse("patients:success_message"))
    
    except Exception as e:
        # في حال حدوث أي خطأ، طباعة تفاصيل الخطأ في السجل وإعادة توجيه المستخدم إلى صفحة الخطأ
        print(f"Error occurred while deleting patient: {str(e)}")
        return redirect(reverse("patients:error_page"))

# عرض تفاصيل المريض
def patient_show_detail(request, pk):
    patient=Patients.objects.filter(id=pk)[0]
    try:
       return render(request, 'patient_info.html', {'patient': patient})
    except:
        return redirect(reverse('patients:error_page'))

# صفحة تعرض رسالة نجاح العملية
def success_message(request):
    return render(request, 'success_message.html')

# صفحة تعرض رسالة خطأ
def error_page(request):
    return render(request, 'error_page.html')
