from django import forms
from .models import FeedbackRound


class FeedbackRoundForm(forms.ModelForm):
    class Meta:
        model = FeedbackRound
        fields = ['name']