from django import forms

from .models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
