from django import forms 

class LoginInputForm(forms.Form):
    username = forms.CharField(label='username', max_length = 50)
    password = forms.CharField(label='password', min_length = 8, max_length = 16, widget = forms.PasswordInput())