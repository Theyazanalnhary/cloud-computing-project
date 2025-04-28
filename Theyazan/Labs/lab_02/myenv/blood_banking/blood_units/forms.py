from django import forms
from .models import BloodUnit
from datetime import date

class BloodUnitForm(forms.ModelForm):
    class Meta:
        model = BloodUnit
        fields = [
            'donor',              # المتبرع
            'blood_type',         # فصيلة الدم
            'donation_date',      # تاريخ التبرع
            'expiry_date',        # تاريخ انتهاء صلاحية الدم
            'status',             # حالة الوحدة
            'quantity',           # الكمية
        ]

        # تخصيص واجهة الإدخال (widgets)
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),  # تاريخ التبرع
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),    # تاريخ انتهاء صلاحية الدم
            'blood_type': forms.Select(choices=BloodUnit.BLOOD_TYPE_CHOICES),  # فصيلة الدم
            'status': forms.Select(choices=BloodUnit.STATUS_CHOICES),  # حالة الوحدة
        }

    def clean_donation_date(self):
        """التحقق من أن تاريخ التبرع لا يكون في المستقبل"""
        donation_date = self.cleaned_data['donation_date']
        if donation_date > date.today():
            raise forms.ValidationError("تاريخ التبرع لا يمكن أن يكون في المستقبل.")
        return donation_date

    def clean_expiry_date(self):
        """التحقق من أن تاريخ انتهاء صلاحية الدم بعد تاريخ التبرع"""
        expiry_date = self.cleaned_data['expiry_date']
        donation_date = self.cleaned_data['donation_date']
        if expiry_date <= donation_date:
            raise forms.ValidationError("تاريخ انتهاء صلاحية الدم يجب أن يكون بعد تاريخ التبرع.")
        return expiry_date

    def clean_quantity(self):
        """التحقق من أن الكمية أكبر من 0"""
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("الكمية يجب أن تكون أكبر من 0.")
        return quantity
