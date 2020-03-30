from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PersonalProject, StructuredProjectCode
from django_ace import AceWidget

"""
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {"username", "email", "password1", "password2"}

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class NewProjectForm(ModelForm):
    class Meta:
        model = PersonalProject
        fields = ['title', 'description', 'code']
"""

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

class NewProjectForm(ModelForm):
    class Meta:
        model = PersonalProject
        fields = ['title', 'description',]


class EditProjectForm(ModelForm):
    class Meta:
        model = PersonalProject
        fields = ['title', 'description','code']
        widgets = {
            'code': AceWidget(mode='python', theme='crimson_editor', width="500px", height="300px",),
        }


class StructuredProjectForm(ModelForm):
    class Meta:
        model = StructuredProjectCode
        fields = ['code']
        widgets = {
            'code': AceWidget(mode='python', theme='crimson_editor', width="700px", height="600px",),
        }