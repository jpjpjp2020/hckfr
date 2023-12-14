from django import forms
from .models import EmployerUser, OversightUser, WorkerUser
from django.contrib.auth.forms import AuthenticationForm


# Reg forms
# Placheholders for orm fields directly in html to keep the front concern seprate

class WorkerUserRegForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = WorkerUser
        fields = ['username', 'password']


class EmployerUserRegForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = EmployerUser
        fields = ['email', 'password', 'oversight_email']

    
class OversightUserRegForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = OversightUser
        fields = ['email', 'password']


# Login forms
# Placheholders for form fields directly in html to keep the front concern seprate

class WorkerUserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())


class EmployerUserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'autofocus': True, 'type': 'email'})

    
class OversightUserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'autofocus': True, 'type': 'email'})