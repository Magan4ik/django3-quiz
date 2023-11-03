from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import MyUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username", "avatar")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("username", "avatar")
