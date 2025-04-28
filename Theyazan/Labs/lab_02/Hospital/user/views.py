# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from patients.views import patients_home  # تأكد من استيراد الصفحة المطلوبة بشكل صحيح

# صفحة تسجيل الدخول
def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patients:home')  # التوجيه إلى الصفحة الرئيسية للنظام بعد تسجيل الدخول
        else:
            return render(request, 'login_form.html', {'error': 'Invalid credentials'})
    return render(request, 'login_form.html')
# صفحة التسجيل
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')  # إعادة التوجيه إلى صفحة تسجيل الدخول بعد التسجيل
    else:
        form = RegisterForm()
    return render(request, 'register_form.html', {'form': form})

# صفحة الخروج
def userlogout(request):
    logout(request)
    return redirect('user:login')  # إعادة التوجيه إلى صفحة تسجيل الدخول بعد الخروج
