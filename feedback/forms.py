from django import forms
from .models import FeedbackRound, Feedback


class FeedbackRoundForm(forms.ModelForm):
    class Meta:
        model = FeedbackRound
        fields = ['name']


class CodeCheckerForm(forms.Form):
    code = forms.CharField(max_length=36, required=True)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 9}),
        }