from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("الاسم الأول"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسمك الأول'})
    )
    last_name = forms.CharField(
        label=_("اسم العائلة"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم العائلة'})
    )
    email = forms.EmailField(
        label=_("البريد الإلكتروني"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'})
    )
    phone_number = forms.CharField(
        label=_("رقم الهاتف"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05xxxxxxxx'})
    )
    address = forms.CharField(
        label=_("العنوان"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'أدخل عنوانك'})
    )
    password1 = forms.CharField(
        label=_("كلمة المرور"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_("تأكيد كلمة المرور"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المستخدم'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تخصيص رسائل المساعدة لحقول كلمة المرور
        self.fields['password1'].help_text = _("""
            • يجب أن تحتوي على 8 أحرف على الأقل
            • لا يمكن أن تكون مشابهة لمعلوماتك الشخصية
            • لا يمكن استخدام كلمات مرور شائعة
            • لا يمكن استخدام أرقام فقط
        """)
        self.fields['password2'].help_text = _("أدخل نفس كلمة المرور للتأكيد")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("هذا البريد الإلكتروني مستخدم بالفعل"))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError(_("يجب أن يحتوي رقم الهاتف على أرقام فقط"))
        if len(phone) < 10:
            raise forms.ValidationError(_("يجب أن يحتوي رقم الهاتف على 10 أرقام على الأقل"))
        return phone

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address') 