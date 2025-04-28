from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Employee
from rest_framework.permissions import IsAuthenticated

# تسجيل الدخول عبر API
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        employee = Employee.objects.get(username=username)
    except Employee.DoesNotExist:
        return JsonResponse({"detail": "Invalid username or password"}, status=400)

    if check_password(password, employee.password):  # استخدام check_password للتحقق من كلمة السر المشفرة
        user, created = User.objects.get_or_create(username=username, email=employee.email)
        if created:
            user.set_password(password)
            user.save()

        login(request, user)
        return JsonResponse({"message": "Login successful"})
    
    return JsonResponse({"detail": "Invalid username or password"}, status=400)

# تسجيل الخروج عبر API
@api_view(['POST'])
def logout_api(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})

# دالة لإضافة موظف (يتمكن المدير فقط من إضافة موظفين)
@api_view(['POST'])
def add_employee(request):
    if request.user.is_authenticated and request.user.employee.role == 'مدير':
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        role = request.data.get('role')
        salary = request.data.get('salary')
        hire_date = request.data.get('hire_date')
        username = request.data.get('username')
        password = request.data.get('password')

        # تأكد من أن كلمة السر مشفرة
        user = User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)  # تأكد من تشفير كلمة السر
        user.save()

        new_employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            role=role,
            salary=salary,
            hire_date=hire_date,
            username=username,
            password=password
        )

        return JsonResponse({"message": "Employee added successfully"})
    return JsonResponse({"detail": "You do not have permission to add employees"}, status=403)

# دالة لتعديل موظف (يتمكن المدير فقط من تعديل الموظفين)
@api_view(['PUT'])
def update_employee(request, employee_id):
    if request.user.is_authenticated and request.user.employee.role == 'مدير':
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({"detail": "Employee not found"}, status=404)

        employee.first_name = request.data.get('first_name', employee.first_name)
        employee.last_name = request.data.get('last_name', employee.last_name)
        employee.email = request.data.get('email', employee.email)
        employee.phone_number = request.data.get('phone_number', employee.phone_number)
        employee.role = request.data.get('role', employee.role)
        employee.salary = request.data.get('salary', employee.salary)
        employee.hire_date = request.data.get('hire_date', employee.hire_date)
        employee.username = request.data.get('username', employee.username)
        employee.password = request.data.get('password', employee.password)

        employee.save()
        return JsonResponse({"message": "Employee updated successfully"})
    return JsonResponse({"detail": "You do not have permission to update employees"}, status=403)

# دالة لحذف موظف (يتمكن المدير فقط من حذف الموظفين)
@api_view(['DELETE'])
def delete_employee(request, employee_id):
    if request.user.is_authenticated and request.user.employee.role == 'مدير':
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({"detail": "Employee not found"}, status=404)

        employee.delete()
        return JsonResponse({"message": "Employee deleted successfully"})
    return JsonResponse({"detail": "You do not have permission to delete employees"}, status=403)
