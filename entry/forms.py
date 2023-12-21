from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


# Reg forms
# Placheholders for form fields directly in html to keep the front concern seprate

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password', 'oversight_value']  # Employer values

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['oversight_value'].required = True


# Login forms
# Placeholder for new logic, but relies on builtin deault auth for now.

class UserLoginForm(AuthenticationForm):

    pass