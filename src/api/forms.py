from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Username"
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password1"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].label = "Password"
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields["password2"].widget.attrs.pop("autofocus", None)
        self.fields["password2"].label = "Confirm password"
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Username"
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password"].widget.attrs.pop("autofocus", None)
        self.fields["password"].label = "Password"

class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Username"
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password1"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].label = "Password"
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields["password2"].widget.attrs.pop("autofocus", None)
        self.fields["password2"].label = "Confirm password"

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            self.add_error("username", "An account with that username does not exist.")
        return cleaned_data
