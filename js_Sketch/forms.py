from django.forms import ModelForm, TextInput, CharField
from .models import Problem, Language


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name',]


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'problemtext', 'solutioncode', 'language']

    # title = CharField(widget=TextInput(attrs={'size':80}))