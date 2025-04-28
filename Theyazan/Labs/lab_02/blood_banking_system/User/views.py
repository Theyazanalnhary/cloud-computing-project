from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User

# عرض جميع المستخدمين
@permission_required('app.view_user', raise_exception=True)
def get_users(request):
    users = User.objects.all()
    users_data = [{"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role} for user in users]
    return JsonResponse({"users": users_data})

# عرض مستخدم معين
@permission_required('app.view_user', raise_exception=True)
def get_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "email": user.email,
        "phone_number": user.phone_number
    }
    return JsonResponse({"user": user_data})

# إضافة مستخدم
@permission_required('app.add_user', raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        role = request.POST.get('role')
        email = request.POST.get('email')

        # تشفير كلمة المرور
        hashed_password = make_password(password)

        # إضافة المستخدم
        user = User.objects.create(username=username, password=hashed_password, full_name=full_name, role=role, email=email)

        return JsonResponse({"message": "User created successfully", "user_id": user.id})

# تعديل مستخدم
@permission_required('app.change_user', raise_exception=True)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.full_name = request.POST.get('full_name', user.full_name)
        user.role = request.POST.get('role', user.role)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        return JsonResponse({"message": "User updated successfully"})

# حذف مستخدم
@permission_required('app.delete_user', raise_exception=True)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({"message": "User deleted successfully"})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# عرض صفحة تسجيل الدخول
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # التحقق من الصلاحيات بعد تسجيل الدخول
                return redirect('home')  # التوجيه إلى الصفحة الرئيسية
            else:
                form.add_error(None, "بيانات الدخول غير صحيحة!")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# صفحة رئيسية (تكون محمية بتسجيل الدخول)
@login_required
def home(request):
    return render(request, 'home.html')
