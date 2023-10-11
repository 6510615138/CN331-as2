from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class createUserForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=25,widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label=_('Email'), max_length=86,widget=forms.TextInput(attrs={'placeholder': 'email'}))
    firstname = forms.CharField(label=_('firstname'), max_length=25,widget=forms.TextInput(attrs={'placeholder': 'firstname'}))
    lastname = forms.CharField(label=_('lastname'), max_length=25,widget=forms.TextInput(attrs={'placeholder': 'lastname'}))
    password = forms.CharField(label=_('Password'), max_length=25, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label=_('Confirm password'), max_length=25, widget=forms.PasswordInput(attrs={'placeholder': 'comfirm password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # Check if passwords match
        if password != password2:
            raise ValidationError(_('Passwords do not match'))

        # Check if the username is already in use
        username = cleaned_data.get('username')
        firstname = cleaned_data.get('firstname')
        lastname = cleaned_data.get('lastname')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('This username is already in use'))

    def create(self):
    
            # Access cleaned form data 
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            firstname = self.cleaned_data['firstname']
            lastname = self.cleaned_data['lastname']
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
    
    
    def createAndLogin(self,request):
    
             # Access cleaned form data 
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            firstname = self.cleaned_data['firstname']
            lastname = self.cleaned_data['lastname']
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            login(request,user)
