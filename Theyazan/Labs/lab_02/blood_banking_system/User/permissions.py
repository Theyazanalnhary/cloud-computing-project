from django.contrib.auth.decorators import permission_required

# عرض المستخدمين فقط للمسؤولين
@permission_required('app.view_user', raise_exception=True)
def get_users(request):
    users = User.objects.all()
    users_data = [{"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role} for user in users]
    return JsonResponse({"users": users_data})

# إضافة مستخدم فقط للمسؤولين
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
