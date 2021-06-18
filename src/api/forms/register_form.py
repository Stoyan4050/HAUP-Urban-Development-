"""
register_form.py
"""

from django.contrib.auth.forms import UserCreationForm
from api.models.user import User


class RegisterForm(UserCreationForm):
    """
    class RegisterForm(UserCreationForm)
    """

    class Meta:
        """
        class Meta
        """

        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """
        def __init__(self, *args, **kwargs)
        """

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
        """
        def save(self, commit=True)
        """

        user = super(RegisterForm, self).save(commit=False)

        if commit:
            user.save()

        return user
