from django import forms
from projects.models import Project, ProjectMember
from uploads.models import Attachment
from django.contrib.auth.models import User

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner','slug')

class AddFileForm(forms.ModelForm):
    class Meta:
        model = Attachment
        exclude = ('project', 'date_created', )


class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'slug')

class AddUserForm(forms.Form):
    LEVELS = (
        ('', '------'),
        ('1', 'Stage 1'),
        ('2', 'Stage 2'),
        ('3', 'Stage 3'),
        ('4', 'Stage 4'),
    )
  
    email = forms.EmailField(required=True)
    level = forms.ChoiceField(choices=LEVELS, required=True)

    def clean_email(self):
        #Check to see if user email exists, if not send email with invite to register
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('User with this email does not exist.')
        return email

class ProjectMemberForm(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = ProjectMember
        exclude = ('project',)
