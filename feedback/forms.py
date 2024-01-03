from django import forms
from .models import FeedbackRound


class FeedbackRoundForm(forms.ModelForm):
    class Meta:
        model = FeedbackRound
        fields = ['name']


class CodeCheckerForm(forms.Form):
    code = forms.CharField(max_length=36, required=True)