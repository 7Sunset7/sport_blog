from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sport'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Athlete
        fields = ['name', 'age', 'content', 'photo', 'sport']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return name


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, required=True)
    email = forms.EmailField(label='Email', required=True)
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required=True)
    captcha = CaptchaField()

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Имя', max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)

