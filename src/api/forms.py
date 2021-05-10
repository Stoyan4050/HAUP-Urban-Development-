from .models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"placeholder": "Email"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Email"
        
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password"].widget.attrs.pop("autofocus", None)
        self.fields["password"].label = "Password"

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["email"].label = "Email"
        
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

class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["email"].label = "Email"
        
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password1"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].label = "Password"
        
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields["password2"].widget.attrs.pop("autofocus", None)
        self.fields["password2"].label = "Confirm password"

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error("email", "An account with that email does not exist.")

        return cleaned_data
