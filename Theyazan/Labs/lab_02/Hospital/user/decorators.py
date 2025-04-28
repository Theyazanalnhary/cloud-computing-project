# accounts/utils.py (أو في views.py)

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# تحقق إذا كان المستخدم في مجموعة "admin"
def isadmin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('401 Unauthorized')  # غير مصرح
        else:
            return HttpResponse('401 Unauthorized')  # غير مصرح
    return wrapper_func

# تحقق إذا كان المستخدم مسجل دخول
def islogin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')  # إعادة التوجيه إلى الصفحة الرئيسية
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
