import re

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
re_phone = re.compile(r'^06[6789][2-9]\d{6}$')


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False, min_length=10, max_length=10)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not re_phone.match(phone):
            raise forms.ValidationError('Incorrect phone number')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('Username already taken')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
