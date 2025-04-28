from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type', 
                 'phone_number', 'department', 'badge_number')

class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_type', 
                 'phone_number', 'department', 'badge_number') 