from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # fields = ("email", "first_name", "last_name", "username", "password1", "password2")
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        # self.fields['first_name'].widget.attrs.update({'placeholder': 'First name'})
        # self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        
        # self.fields['email'].widget.attrs.pop("autofocus", None)
        # self.fields['first_name'].widget.attrs.pop("autofocus", None)
        # self.fields['last_name'].widget.attrs.pop("autofocus", None)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['password1'].widget.attrs.pop("autofocus", None)
        self.fields['password2'].widget.attrs.pop("autofocus", None)
        
        # self.fields['email'].label = 'Email'
        # self.fields['first_name'].label = 'First name'
        # self.fields['last_name'].label = 'Last name'
        self.fields['username'].label = 'Username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm password'
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
