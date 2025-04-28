# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# عرض جميع المستخدمين
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# عرض تفاصيل مستخدم معين
def user_detail(request, userid):
    user = get_object_or_404(User, userid=userid)
    return render(request, 'user_detail.html', {'user': user})

# API لعرض جميع المستخدمين
@api_view(['GET'])
def user_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# API لعرض تفاصيل مستخدم معين
@api_view(['GET'])
def user_detail_api(request, userid):
    try:
        user = User.objects.get(userid=userid)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# دالة لإضافة مستخدم جديد
@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        # الحصول على البيانات من الـ JSON
        data = request.data

        # التحقق من أن جميع الحقول موجودة
        required_fields = ['fname', 'sname', 'loginname', 'password', 'email', 'role']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'حقل {field} مفقود'}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء كائن المستخدم
        user = User(
            fname=data['fname'],
            sname=data['sname'],
            loginname=data['loginname'],
            password=data['password'],  # سنقوم بتشفير كلمة المرور في الـ save method
            email=data.get('email', None),
            phone=data.get('phone', None),
            country=data.get('country', None),
            role=data['role'],
        )

        try:
            # التحقق من صحة البيانات
            user.clean()  # يتم هنا تنفيذ دالة الـ clean في الموديل للتحقق من صحة كلمة المرور
            user.save()
            return Response({'message': 'تم إضافة المستخدم بنجاح'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# دالة لتعديل بيانات مستخدم معين
@api_view(['PUT'])
def update_user(request, userid):
    try:
        user = User.objects.get(userid=userid)
    except User.DoesNotExist:
        return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    # الحصول على البيانات من الطلب
    data = request.data

    # تحديث البيانات المطلوبة
    if 'fname' in data:
        user.fname = data['fname']
    if 'sname' in data:
        user.sname = data['sname']
    if 'loginname' in data:
        user.loginname = data['loginname']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'country' in data:
        user.country = data['country']
    if 'role' in data:
        user.role = data['role']
    if 'password' in data:
        # إذا تم تعديل كلمة المرور، نقوم بتشفيرها
        user.password = make_password(data['password'])

    try:
        # التحقق من صحة البيانات باستخدام الـ clean method
        user.clean()
        user.save()
        return Response({'message': 'تم تعديل البيانات بنجاح'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# دالة لحذف مستخدم معين
@api_view(['DELETE'])
def delete_user(request, userid):
    try:
        user = User.objects.get(userid=userid)
    except User.DoesNotExist:
        return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    # حذف المستخدم من قاعدة البيانات
    user.delete()
    return Response({'message': 'تم حذف المستخدم بنجاح'}, status=status.HTTP_204_NO_CONTENT)

# دالة لتسجيل الدخول
@api_view(['POST'])
def login_user(request):
    # الحصول على اسم المستخدم وكلمة المرور من الطلب
    loginname = request.data.get('loginname')
    password = request.data.get('password')

    if not loginname or not password:
        return Response({'error': 'اسم المستخدم أو كلمة المرور مفقودة'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(loginname=loginname)
    except User.DoesNotExist:
        return Response({'error': 'اسم المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    # التحقق من كلمة المرور
    if not check_password(password, user.password):
        return Response({'error': 'كلمة المرور غير صحيحة'}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق إذا كان المستخدم مديرًا أم عاديًا
    if user.is_admin():
        return Response({'message': 'تم تسجيل الدخول كمدير', 'role': 'admin'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'تم تسجيل الدخول كمستخدم عادي', 'role': 'user'}, status=status.HTTP_200_OK)
