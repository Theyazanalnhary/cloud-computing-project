from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
       firstD_name = forms.CharField(
        label="First Name", 
        widget=forms.TextInput(), 
        required=True,
        initial='Doctor',
        help_text="This is the patient's first name"
    )
       lastD_name = forms.CharField(  # تعديل second_name إلى last_name
        label="Last Name", 
        widget=forms.TextInput(), 
        required=True,
        initial='Doctor',
        help_text="This is the patient's last name"
    )
       age = forms.IntegerField(
        label="Age", 
        widget=forms.NumberInput(), 
        required=True, 
        initial="20"
    )

       specialization = forms.CharField(
        label="specialization",
        widget=forms.TextInput,
        required=False,
       ) 
      
       image = forms.ImageField(
        label="Image", 
        widget=forms.ClearableFileInput(), 
        required=False
    )
       file_report = forms.FileField(
        label="File Report", 
        widget=forms.ClearableFileInput(), 
        required=False
    )
       bio = forms.CharField(
        label="bio", 
        widget=forms.Textarea(), 
        required=False
    )

       class Meta:
        model = Doctor
        fields = ['firstD_name', 'lastD_name', 'age', 'specialization', 'image', 'file_report', 'bio']
