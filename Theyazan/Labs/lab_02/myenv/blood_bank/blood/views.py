# blood_donation/views.py
from rest_framework import generics
from .models import Donor
from .serializers import DonorSerializer
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response

# إضافة متبرع جديد
class DonorCreateView(generics.CreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

# جلب المتبرعين
class DonorListView(generics.ListAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

# تحديث معلومات المتبرع
class DonorUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

# blood_donation/views.py



class DonorDeleteView(generics.DestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            # الحصول على المتبرع الذي سيتم حذفه بناءً على المعرف (pk)
            instance = self.get_object()
            self.perform_destroy(instance)  # حذف المتبرع من قاعدة البيانات
            return Response({"message": "تم حذف المتبرع بنجاح"}, status=status.HTTP_204_NO_CONTENT)
        except Donor.DoesNotExist:
            # إذا لم يتم العثور على المتبرع، رد برسالة خطأ
            return Response({"error": "المتبرع غير موجود"}, status=status.HTTP_404_NOT_FOUND)

# البحث عن متبرعين
class DonorSearchView(generics.ListAPIView):
    serializer_class = DonorSerializer

    def get_queryset(self):
        blood_type = self.request.query_params.get('blood_type', None)
        if blood_type:
            return Donor.objects.filter(blood_type__iexact=blood_type)
        return Donor.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response['Content-Type'] = 'application/json; charset=UTF-8'
        return response

# جلب المتبرعين بناءً على تاريخ التبرع أو الصلاحية
class DonorByDateView(generics.ListAPIView):
    serializer_class = DonorSerializer

    def get_queryset(self):
        today = now().date()
        return Donor.objects.filter(expiration_date__gte=today)





class RareBloodTypesView(generics.ListAPIView):
    serializer_class = DonorSerializer

    def get_queryset(self):
        rare_blood_threshold = 10
        return Donor.objects.filter(quantity__lt=rare_blood_threshold)