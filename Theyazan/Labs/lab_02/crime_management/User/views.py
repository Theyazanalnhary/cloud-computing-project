from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import PoliceOfficer
from .forms import PoliceOfficerForm

# التحقق من الدور
def is_manager(user):
    return hasattr(user, 'policeofficer') and user.policeofficer.role == 'مدير'

def is_data_entry(user):
    return hasattr(user, 'policeofficer') and user.policeofficer.role == 'مدخل بيانات'

def is_editor(user):
    return hasattr(user, 'policeofficer') and user.policeofficer.role == 'معدل'

def is_report(user):
    return hasattr(user, 'policeofficer') and user.policeofficer.role == 'مسؤول تقارير'

# إنشاء ضابط جديد
@login_required
@user_passes_test(is_manager)
def create_officer(request):
    if request.method == 'POST':
        form = PoliceOfficerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)

            officer = form.save(commit=False)
            officer.user = user
            officer.created_by = request.user  # تحديد من أنشأ السجل
            officer.save()
            return redirect('officer_list')
    else:
        form = PoliceOfficerForm()
    return render(request, 'create.html', {'form': form})

# تعديل ضابط
@login_required
@user_passes_test(is_manager)
def edit_officer(request, officer_id):
    officer = get_object_or_404(PoliceOfficer, id=officer_id)
    if request.method == 'POST':
        form = PoliceOfficerForm(request.POST, instance=officer)
        if form.is_valid():
            officer = form.save(commit=False)
            officer.updated_by = request.user  # تحديد من عدل السجل
            officer.save()
            return redirect('officer_list')
    else:
        form = PoliceOfficerForm(instance=officer)
    return render(request, 'edit.html', {'form': form})

# حذف ضابط
@login_required
@user_passes_test(is_manager)
def delete_officer(request, officer_id):
    officer = get_object_or_404(PoliceOfficer, id=officer_id)
    officer.user.delete()
    officer.delete()
    return redirect('officer_list')

# قائمة الضباط
@login_required
@user_passes_test(is_manager)
def officer_list(request):
    officers = PoliceOfficer.objects.all()
    return render(request, 'list.html', {'officers': officers})

from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import render, redirect

class CustomLoginView(LoginView):
    template_name = 'login.html'  # صفحة تسجيل الدخول

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        fail_key = f"failures_{username}"
        attempts = cache.get(fail_key, 0)

        # التحقق من عدد المحاولات المسموح بها
        if attempts >= 5:  # إذا تجاوز عدد المحاولات 5
            return render(self.request, 'login_blocked.html')  # عرض صفحة محظور الوصول

        # حذف عدد المحاولات بعد النجاح
        cache.delete(fail_key)

        # تسجيل الدخول باستخدام الطريقة الافتراضية
        response = super().form_valid(form)

        # إعادة توجيه المستخدم إلى الصفحة الرئيسية
        return redirect('index')  # تأكد من أن اسم المسار هو 'index'
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # جلب بيانات المستخدم الحالي
    user = request.user
    try:
        officer = user.policeofficer  # ربط الضابط بالمستخدم
        role = officer.role
    except AttributeError:
        role = "غير محدد"  # إذا لم يكن للمستخدم دور محدد

    context = {
        'user': user,
        'role': role,
    }
    return render(request, 'index.html', context)