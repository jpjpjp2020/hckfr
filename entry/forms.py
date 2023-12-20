from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


# Reg forms
# Placheholders for form fields directly in html to keep the front concern seprate

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'oversight_value']  # All pos fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['username'].required = False
        self.fields['oversight_value'].required = False


# Login forms
# Placheholders for form fields directly in html to keep the front concern seprate

class UserLoginForm(AuthenticationForm):

    role = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):

        super().clean()

        role = self.cleaned_data.get('role')

        if role == 'worker':
            username = self.cleaned_data.get('username')
        else:
            email = self.cleaned_data.get('username')
        return self.cleaned_data