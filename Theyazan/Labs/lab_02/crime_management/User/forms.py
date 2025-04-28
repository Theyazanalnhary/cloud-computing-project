from django import forms
from .models import PoliceOfficer,User

class PoliceOfficerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="اسم المستخدم")
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة المرور")

    class Meta:
        model = PoliceOfficer
        fields = ['officer_number', 'full_name', 'rank', 'id_number', 'role']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        id_number = cleaned_data.get('id_number')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'اسم المستخدم موجود مسبقاً')
        if PoliceOfficer.objects.filter(id_number=id_number).exists():
            self.add_error('id_number', 'رقم الهوية موجود مسبقاً')