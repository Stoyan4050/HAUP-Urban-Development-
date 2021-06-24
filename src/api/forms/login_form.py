"""
login_form.py
"""

from django.contrib.auth.forms import AuthenticationForm
from api.models.user import User


class LoginForm(AuthenticationForm):
    """
    class LoginForm(AuthenticationForm)
    """

    class Meta:
        """
        class Meta
        """

        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        """
        def __init__(self, *args, **kwargs)
        """

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"placeholder": "Email address"})
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].label = "Email address"

        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password"].widget.attrs.pop("autofocus", None)
        self.fields["password"].label = "Password"
