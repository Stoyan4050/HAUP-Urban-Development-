"""
test_register_form.py
"""

import unittest
from unittest.mock import patch
from api.forms.register_form import RegisterForm
from api.models.user import User


class TestRegisterForm(unittest.TestCase):
    """
    class TestRegisterForm(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user_credentials = {
            "username": "username",
            "password": "password",
        }
        self.register_form = RegisterForm()

    def test_register_form_init(self):
        """
        def test_register_form_init(self)
        """

        self.assertEqual(self.register_form.fields["email"].widget.attrs.get("placeholder"), "Email address")
        self.assertEqual(self.register_form.fields["email"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.register_form.fields["email"].label, "Email address")

        self.assertEqual(self.register_form.fields["password1"].widget.attrs.get("placeholder"), "Password")
        self.assertEqual(self.register_form.fields["password1"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.register_form.fields["password1"].label, "Password")

        self.assertEqual(self.register_form.fields["password2"].widget.attrs.get("placeholder"), "Confirm password")
        self.assertEqual(self.register_form.fields["password2"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.register_form.fields["password2"].label, "Confirm password")

    @patch("api.forms.register_form.UserCreationForm.save")
    def test_register_form_save_commit_false(self, mock_form_save):
        """
        @patch("api.forms.register_form.UserCreationForm.save")
        def test_register_form_save_commit_false(self, mock_form_save)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_form_save.return_value = user

        self.assertEqual(self.register_form.save(commit=False), user)
        mock_form_save.assert_called_once_with(commit=False)

    @patch("api.forms.register_form.User.save")
    @patch("api.forms.register_form.UserCreationForm.save")
    def test_register_form_save_commit_true(self, mock_form_save, mock_user_save):
        """
        @patch("api.forms.register_form.User.save")
        @patch("api.forms.register_form.UserCreationForm.save")
        def test_register_form_save_commit_true(self, mock_form_save, mock_user_save)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_form_save.return_value = user
        mock_user_save.return_value = None

        self.assertEqual(self.register_form.save(commit=True), user)
        mock_form_save.assert_called_once_with(commit=False)
        mock_user_save.assert_called_once_with()
