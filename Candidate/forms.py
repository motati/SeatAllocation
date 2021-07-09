from django import forms
from django.contrib.auth.models import User
from .models import *


class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('rollnumber', 'category', 'birthdate', 'phone', 'rank', 'gender', 'email')


class FreezeForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('rollnumber', 'rank')
