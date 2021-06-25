"""
test_new_password_form.py
"""

import unittest
from api.forms.new_password_form import NewPasswordForm
from api.models.user import User


class TestNewPasswordForm(unittest.TestCase):
    """
    class TestNewPasswordForm(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.new_password_form = NewPasswordForm(User(email="username", password="password"))

    def test_new_password_form_init(self):
        """
        def test_new_password_form_init(self)
        """

        self.assertEqual(self.new_password_form.fields["new_password1"].widget.attrs.get("placeholder"),
                         "New password")
        self.assertEqual(self.new_password_form.fields["new_password1"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.new_password_form.fields["new_password1"].label, "New password")

        self.assertEqual(self.new_password_form.fields["new_password2"].widget.attrs.get("placeholder"),
                         "Confirm new password")
        self.assertEqual(self.new_password_form.fields["new_password2"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.new_password_form.fields["new_password2"].label, "Confirm new password")
