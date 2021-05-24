from .models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"placeholder": "Email address"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Email address"

        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password"].widget.attrs.pop("autofocus", None)
        self.fields["password"].label = "Password"


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Email address"})
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["email"].label = "Email address"

        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password1"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].label = "Password"

        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm password"})
        self.fields["password2"].widget.attrs.pop("autofocus", None)
        self.fields["password2"].label = "Confirm password"

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class ChangePasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Email address"})
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["email"].label = "Email address"

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")

        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            self.add_error("email", "An account with that email address does not exist.")

        return cleaned_data


class NewPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ("new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({"placeholder": "New password"})
        self.fields["new_password1"].widget.attrs.pop("autofocus", None)
        self.fields["new_password1"].label = "New password"

        self.fields["new_password2"].widget.attrs.update({"placeholder": "Confirm new password"})
        self.fields["new_password2"].widget.attrs.pop("autofocus", None)
        self.fields["new_password2"].label = "Confirm new password"
