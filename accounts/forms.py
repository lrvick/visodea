from django import forms
from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField 
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser', 'password','last_login','date_joined')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserCreationFormExtended(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name')

class UserProfileForm1(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('company','title','url','background','performance')

class UserProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_home','phone_office','phone_mobile','street_line1','street_line2','city','state','zip','country')
