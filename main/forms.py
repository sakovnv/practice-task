from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from main.models import User
from main.utils import form_attr


class RegisterForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=form_attr))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs=form_attr))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs=form_attr))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs=form_attr))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=form_attr))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs=form_attr))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=form_attr))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=form_attr))


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Choose File')
