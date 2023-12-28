from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import re


# Reg forms
# Placheholders for form fields directly in html to keep the front concern seprate

class WorkerRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        print("clean_username: username =", username)

        # Min-char check
        min_length = 6
        if len(username) < min_length:
            raise ValidationError(f"Username must be at least {min_length} characters long.")

        # Allowed char_check
        if not re.match("^[a-zA-Z0-9_.]*$", username):
            raise ValidationError("Username can only contain alphanumeric characters, underscores, and periods.")

        return username
    
    def clean(self):
        cleaned_data = super().clean()
        print("clean: cleaned_data =", cleaned_data)

        # Set role on the form's instance
        self.instance.role = 'worker'

        return cleaned_data


class EmployerRegForm(forms.ModelForm):
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
    

class OversightRegform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']  # Oversight values

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # Clean method of the User model
        user = User(email=email)
        user.clean()
        print("clean: cleaned_data =", cleaned_data)
        return cleaned_data

    
# login forms
# Custom login form placeholder for employer and oversight for pos integrations

class UserLoginForm(AuthenticationForm):

    pass


# Separate employeeworker login form

class WorkerLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Authenticate with with username and password
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data