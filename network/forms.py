import re

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserLoginForm(AuthenticationForm):
    pass


class UserRegisterForm(forms.Form):
    """
        add form-control class to all fields
    """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attr.get('class'):
                field.widget.attr['class'] += 'form-control'
            else:
                field.widget.attr['class'] = 'form-control'

    username = forms.CharField()
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords are not equal')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r"[^@]+@gmail\.com$", email):
            raise ValidationError('Only Gmail addresses are allowed.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
