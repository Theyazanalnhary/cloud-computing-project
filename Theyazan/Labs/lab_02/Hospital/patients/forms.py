from django import forms
from .models import Patients

class PatientsForm(forms.Form):
    first_name = forms.CharField(
        label="First Name", 
        widget=forms.TextInput(), 
        required=True,
        initial='patients',
        help_text="This is the patient's first name"
    )
    last_name = forms.CharField(  # تعديل second_name إلى last_name
        label="Last Name", 
        widget=forms.TextInput(), 
        required=True,
        initial='patients',
        help_text="This is the patient's last name"
    )
    age = forms.IntegerField(
        label="Age", 
        widget=forms.NumberInput(), 
        required=True, 
        initial="20"
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
    report = forms.CharField(
        label="Report", 
        widget=forms.Textarea(), 
        required=False
    )

class PatientsForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['first_name', 'last_name', 'age', 'image', 'file_report', 'report']