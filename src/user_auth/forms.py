from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, required=False, label=_('Phone Number'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']
