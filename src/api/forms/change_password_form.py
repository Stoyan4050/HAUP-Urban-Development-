"""
change_password_form.py
"""

from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ObjectDoesNotExist
from api.models.user import User


class ChangePasswordForm(PasswordResetForm):
    """
    class ChangePasswordForm(PasswordResetForm)
    """

    class Meta:
        """
        class Meta
        """

        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        """
        def __init__(self, *args, **kwargs)
        """

        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Email address"})
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["email"].label = "Email address"

    def clean(self):
        """
        def clean(self)
        """

        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")

        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            self.add_error("email", "An account with that email address does not exist.")

        return cleaned_data
