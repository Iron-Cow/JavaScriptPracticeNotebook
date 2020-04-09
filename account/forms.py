from django.forms import ModelForm, TextInput, CharField
from .models import Feedback
from django import forms


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'content']


class FeedbackFilterForm(forms.Form):
    pending = forms.BooleanField(label="pending")
    answered = forms.BooleanField(label="answered")
    deleted_by_user = forms.BooleanField(label="deleted_by_user")
    ignored = forms.BooleanField(label="ignored")
    q = forms.CharField(max_length=100)

