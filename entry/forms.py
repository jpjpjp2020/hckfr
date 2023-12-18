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
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())

    # Override the builtin fallback messages.
    # error_messages = {
    #     'invalid_login': _("Please enter correct credentials. "
    #                        "Note that fields may be case-sensitive."),
    # }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # Override the label for the 'username' field to 'Email'
        self.fields['username'].label = "Email"