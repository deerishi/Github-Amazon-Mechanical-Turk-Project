from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username=forms.CharField(label="username")
    #email=forms.EmailField(label="Your email address", required=True)
    #first_name=forms.CharField(label="First Name")
    #last_name=forms.CharField(label="Last Name")
    password1=forms.CharField(label="Password", widget = forms.PasswordInput())
    password2=forms.CharField(label="Confirm Password", widget = forms.PasswordInput())
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print('Email exists in form')
            raise forms.ValidationError("This email has already registered.")
        return email
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            print('User exists in form')
            raise forms.ValidationError("This username has already registered.")
        return username

class FeedBackForm(forms.Form):
    feedback=forms.CharField(widget=forms.Textarea, required=True)
