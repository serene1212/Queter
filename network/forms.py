from django.contrib.auth.forms import AuthenticationForm
from django import forms


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

    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

