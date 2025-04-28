from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()  # استرجاع جميع العملاء
    serializer_class = CustomerSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لعرض جميع العملاء عبر API (GET)
    def list(self, request):
        customers = self.get_queryset()  # جلب جميع العملاء
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    # دالة لعرض عميل معين عبر API (GET)
    def retrieve(self, request, pk=None):
        customer = self.get_object()  # جلب العميل باستخدام المعرف (PK)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    # دالة لإضافة عميل جديد عبر API (POST)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)  # جلب البيانات من الطلب
        if serializer.is_valid():  # التحقق من صحة البيانات
            serializer.save()  # حفظ العميل الجديد
            return Response(serializer.data, status=201)  # إرجاع البيانات المضافة
        return Response(serializer.errors, status=400)  # في حالة وجود خطأ في البيانات

    # دالة لتعديل بيانات عميل عبر API (PUT)
    def update(self, request, pk=None):
        customer = self.get_object()  # جلب العميل باستخدام المعرف (PK)
        serializer = self.get_serializer(customer, data=request.data, partial=False)  # تحديث البيانات بالكامل
        if serializer.is_valid():
            serializer.save()  # حفظ التعديلات
            return Response(serializer.data, status=200)  # إرجاع البيانات المعدلة
        return Response(serializer.errors, status=400)  # في حالة وجود خطأ في البيانات

    # دالة لتعديل بيانات عميل جزئياً عبر API (PATCH)
    def partial_update(self, request, pk=None):
        customer = self.get_object()  # جلب العميل باستخدام المعرف (PK)
        serializer = self.get_serializer(customer, data=request.data, partial=True)  # تحديث البيانات جزئياً
        if serializer.is_valid():
            serializer.save()  # حفظ التعديلات
            return Response(serializer.data, status=200)  # إرجاع البيانات المعدلة
        return Response(serializer.errors, status=400)  # في حالة وجود خطأ في البيانات

    # دالة لحذف عميل عبر API (DELETE)
    def destroy(self, request, pk=None):
        customer = self.get_object()  # جلب العميل باستخدام المعرف (PK)
        customer.delete()  # حذف العميل
        return Response({'message': 'Customer deleted successfully'}, status=204)  # إرجاع رسالة نجاح
