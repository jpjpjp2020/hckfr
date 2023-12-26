from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        oversight_value = cleaned_data.get("oversight_value")

        if email == oversight_value:
            self.add_error('oversight_value', "Oversight email cannot be the same as your email.")

        # Clean method of the User model
        user = User(email=email, oversight_value=oversight_value)
        user.clean()

        return cleaned_data


# Login forms
# Placeholder for new logic, but relies on builtin deault auth for now.

class UserLoginForm(AuthenticationForm):

    pass