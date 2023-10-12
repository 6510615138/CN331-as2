from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.models import Scholar

User = get_user_model()

class createUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(max_length = 200) 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(createUserForm, self).save(commit=False)  # Use the correct class name
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        scholar = Scholar(ID=user, scholar_name=user.get_full_name(), scholar_email=user.email)
        if commit:
            user.save()
            scholar.save()
        return user 