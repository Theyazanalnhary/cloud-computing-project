from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib import messages
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Staff
from .serializers import StaffSerializer
from .permissions import IsSupervisor
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView

# تسجيل الدخول
class LoginView(View):
    def get(self, request):
        return render(request, 'Templates staff/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "اسم المستخدم وكلمة المرور مطلوبة.")
            return redirect('staff:login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "بيانات الاعتماد غير صحيحة.")
            return redirect('staff:login')

        try:
            staff_member = Staff.objects.get(user=user)
            login(request, user)

            # التحقق من الدور
            if staff_member.is_supervisor:  # إذا كان مديرًا
                return redirect('staff:home')  # صفحة المدير
            else:  # إذا كان موظفًا
                return redirect('staff:home')  # نفس الصفحة مع إخفاء إدارة الموظفين

        except Staff.DoesNotExist:
            messages.error(request, "الموظف غير موجود.")
            return redirect('staff:login')


# تسجيل الخروج
def logout_view(request):
    logout(request)
    return redirect('staff:login')


# عرض الصفحة الرئيسية مع شريط علوي ديناميكي
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # التحقق من صلاحيات المستخدم
        staff_member = Staff.objects.get(user=self.request.user)
        context['is_supervisor'] = staff_member.is_supervisor  # تمرير صلاحية المدير
        return context


# إضافة موظف جديد (للمشرفين فقط)
class CreateStaffView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsSupervisor]

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()
        serializer.save(user=user)


# عرض قائمة الموظفين
class StaffListView(ListView):
    model = Staff
    template_name = 'Templates staff/staff_list.html'
    context_object_name = 'staff_members'

    def get_queryset(self):
        return Staff.objects.all()  # يمكنك تخصيص هذا الاستعلام حسب الحاجة


# حذف موظف
class DeleteStaffView(APIView):
    permission_classes = [IsSupervisor]  # التأكد من أن المشرف هو الذي يقوم بالحذف

    def delete(self, request, staff_id):
        try:
            # البحث عن الموظف باستخدام الـ ID
            staff_member = Staff.objects.get(id=staff_id)
            staff_member.delete()  # حذف الموظف من قاعدة البيانات
            return Response({"message": "تم الحذف بنجاح!"}, status=status.HTTP_204_NO_CONTENT)
        except Staff.DoesNotExist:
            return Response({"error": "الموظف غير موجود."}, status=status.HTTP_404_NOT_FOUND)


# تعديل موظف
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        # تحديث بيانات الموظف
        staff.user.username = request.POST.get('username')
        staff.phone_number = request.POST.get('phone_number')
        staff.date_of_joining = request.POST.get('date_of_joining')
        staff.role = request.POST.get('role')

        # تحديث كلمة المرور إذا كانت موجودة
        password = request.POST.get('password')
        if password:
            staff.user.set_password(password)
        
        staff.user.save()  # حفظ التغييرات على المستخدم
        staff.save()  # حفظ التغييرات على الموظف

        return redirect('staff:staff_list')  # إعادة توجيه إلى قائمة الموظفين بعد التحديث

    return render(request, 'Template staff/edit_staff.html', {'staff': staff})