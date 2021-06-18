"""
new_password_form.py
"""

from django.contrib.auth.forms import SetPasswordForm
from api.models.user import User


class NewPasswordForm(SetPasswordForm):
    """
    class NewPasswordForm(SetPasswordForm)
    """

    class Meta:
        """
        class Meta
        """

        model = User
        fields = ("new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        """
        def __init__(self, *args, **kwargs)
        """

        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({"placeholder": "New password"})
        self.fields["new_password1"].widget.attrs.pop("autofocus", None)
        self.fields["new_password1"].label = "New password"

        self.fields["new_password2"].widget.attrs.update({"placeholder": "Confirm new password"})
        self.fields["new_password2"].widget.attrs.pop("autofocus", None)
        self.fields["new_password2"].label = "Confirm new password"
