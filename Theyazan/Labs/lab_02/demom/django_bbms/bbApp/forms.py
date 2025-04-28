from django import forms
from blood_requests.models import BloodRequest
from blood_units.models import BloodUnit

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'name',               # اسم مقدم الطلب
            'email',              # البريد الإلكتروني
            'phone_number',       # رقم الهاتف
            'blood_type',         # فصيلة الدم
            'quantity',           # الكمية المطلوبة
            'status',             # حالة الطلب
        ]

        # تخصيص واجهة الإدخال (widgets)
        widgets = {
            'blood_type': forms.Select(choices=BloodRequest.BLOOD_TYPE_CHOICES),  # فصيلة الدم
            'status': forms.Select(choices=BloodRequest.STATUS_CHOICES),  # حالة الطلب
        }

    def clean_quantity(self):
        """التحقق من أن الكمية المطلوبة أكبر من 0"""
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("الكمية يجب أن تكون أكبر من 0.")
        return quantity

    def clean_blood_type(self):
        """التحقق من أن فصيلة الدم المدخلة موجودة في المخزون لوحدات الدم"""
        blood_type = self.cleaned_data['blood_type']
        # التحقق من أن هناك وحدات دم بهذا النوع في المخزون
        if not BloodUnit.objects.filter(blood_type=blood_type).exists():
            raise forms.ValidationError(f"لا يوجد وحدات دم من فصيلة {blood_type} في المخزون.")
        return blood_type

    def clean_status(self):
        """التحقق من أن حالة الطلب هي حالة صالحة"""
        status = self.cleaned_data['status']
        if status not in dict(BloodRequest.STATUS_CHOICES):
            raise forms.ValidationError("الحالة المدخلة غير صالحة.")
        return status

    def clean(self):
        """التحقق من توفر الكمية المطلوبة بناءً على المخزون"""
        cleaned_data = super().clean()
        quantity_required = cleaned_data.get('quantity')
        blood_type = cleaned_data.get('blood_type')

        if blood_type and quantity_required:
            # نحصل على وحدات الدم المتاحة من نفس فصيلة الدم المطلوبة
            available_blood_units = BloodUnit.objects.filter(blood_type=blood_type)
            total_available_quantity = sum(unit.quantity for unit in available_blood_units)

            # التحقق من أن الكمية المطلوبة أقل من أو تساوي الكمية المتاحة
            if total_available_quantity < quantity_required:
                raise forms.ValidationError(
                    f"الكمية المطلوبة ({quantity_required}) أكبر من الكمية المتوفرة في المخزون ({total_available_quantity})."
                )
        return cleaned_data
