from django import forms
from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField 
from uploads.models import Attachment
from django.contrib.auth.models import User

class Addfileform(forms.ModelForm):
    class Meta:
        model = Attachment

