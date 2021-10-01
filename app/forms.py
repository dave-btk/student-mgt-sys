from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import Students
from .models import SessionYearModel, Courses
User = get_user_model()


class SignUpUsers(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'user_type', 'email']
        labels = {'email': 'Email ID'}

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        # fields = "__all__"
        fields = ['gender', 'address']

        widgets = {
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }