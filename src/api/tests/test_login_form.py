"""
test_login_form.py
"""

import unittest
from api.forms.login_form import LoginForm


class TestLoginForm(unittest.TestCase):
    """
    class TestLoginForm(unittest.TestCase)
    """

    def test_login_form(self):
        """
        def test_login_form(self)
        """

        login_form = LoginForm()

        self.assertEqual(login_form.fields["username"].widget.attrs.get("placeholder"), "Email address")
        self.assertEqual(login_form.fields["username"].widget.attrs.get("autofocus"), None)
        self.assertEqual(login_form.fields["username"].label, "Email address")

        self.assertEqual(login_form.fields["password"].widget.attrs.get("placeholder"), "Password")
        self.assertEqual(login_form.fields["password"].widget.attrs.get("autofocus"), None)
        self.assertEqual(login_form.fields["password"].label, "Password")
