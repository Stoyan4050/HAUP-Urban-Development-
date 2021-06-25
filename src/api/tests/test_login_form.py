"""
test_login_form.py
"""

import unittest
from api.forms.login_form import LoginForm


class TestLoginForm(unittest.TestCase):
    """
    class TestLoginForm(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.login_form = LoginForm()

    def test_login_form_init(self):
        """
        def test_login_form_init(self)
        """

        self.assertEqual(self.login_form.fields["username"].widget.attrs.get("placeholder"), "Email address")
        self.assertEqual(self.login_form.fields["username"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.login_form.fields["username"].label, "Email address")

        self.assertEqual(self.login_form.fields["password"].widget.attrs.get("placeholder"), "Password")
        self.assertEqual(self.login_form.fields["password"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.login_form.fields["password"].label, "Password")
