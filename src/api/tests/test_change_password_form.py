"""
test_change_password_form.py
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from django.core.exceptions import ObjectDoesNotExist
from api.forms.change_password_form import ChangePasswordForm
from api.models.user import User


class TestChangePasswordForm(unittest.TestCase):
    """
    class TestChangePasswordForm(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user_credentials = {
            "email": "email",
            "password": "password",
        }
        self.change_password_form = ChangePasswordForm()

    def test_change_password_form_init(self):
        """
        def test_change_password_form_init(self)
        """

        self.assertEqual(self.change_password_form.fields["email"].widget.attrs.get("placeholder"), "Email address")
        self.assertEqual(self.change_password_form.fields["email"].widget.attrs.get("autofocus"), None)
        self.assertEqual(self.change_password_form.fields["email"].label, "Email address")

    @patch("api.forms.change_password_form.User")
    def test_change_password_form_clean_user_error(self, mock_user):
        """
        @patch("api.forms.change_password_form.User")
        def test_change_password_form_clean_user_error(self, mock_user)
        """

        mock_cleaned_data = PropertyMock(return_value=self.user_credentials)
        type(self.change_password_form).cleaned_data = mock_cleaned_data
        mock_user.objects.get = MagicMock(side_effect=ObjectDoesNotExist("Exception."))
        self.change_password_form.add_error = MagicMock(return_value=None)

        self.assertEqual(self.change_password_form.clean(), self.user_credentials)
        mock_cleaned_data.assert_called_once_with()
        mock_user.objects.get.assert_called_once_with(email=self.user_credentials["email"])
        error = "An account with that email address does not exist."
        self.change_password_form.add_error.assert_called_once_with("email", error)

    @patch("api.forms.change_password_form.User")
    def test_change_password_form_clean_user_valid(self, mock_user):
        """
        @patch("api.forms.change_password_form.User")
        def test_change_password_form_clean_user_valid(self, mock_user)
        """

        user = User(email=self.user_credentials["email"], password=self.user_credentials["password"])

        mock_cleaned_data = PropertyMock(return_value=self.user_credentials)
        type(self.change_password_form).cleaned_data = mock_cleaned_data
        mock_user.objects.get.return_value = user

        self.assertEqual(self.change_password_form.clean(), self.user_credentials)
        mock_cleaned_data.assert_called_once_with()
        mock_user.objects.get.assert_called_once_with(email=self.user_credentials["email"])
