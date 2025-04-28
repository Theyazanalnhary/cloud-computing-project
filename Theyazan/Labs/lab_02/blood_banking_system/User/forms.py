from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'role', 'email', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        }
    
    # لإظهار كلمة المرور بشكل مؤمن
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("This field is required")
        return make_password(password)
