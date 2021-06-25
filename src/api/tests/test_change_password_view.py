"""
test_change_password_view.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from django.test import RequestFactory
from api.models.user import User
from api.views.change_password_view import ChangePasswordView


class TestChangePasswordView(unittest.TestCase):
    """
    class TestChangePasswordView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user_credentials = {
            "email": "email",
            "password": "password",
        }
        self.request_factory = RequestFactory()

    def test_change_password_view_get_request(self):
        """
        def test_change_password_view_get_request(self)
        """

        request = self.request_factory.get("/urban_development/change_password/")
        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    @patch("api.views.change_password_view.ChangePasswordForm")
    def test_change_password_view_post_request_form_invalid(self, mock_change_password_form):
        """
        @patch("api.views.change_password_view.ChangePasswordForm")
        def test_change_password_view_post_request_form_invalid(self, mock_change_password_form)
        """

        mock_change_password_form.return_value.is_valid.return_value = False

        request = self.request_factory.post("/urban_development/change_password/")
        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        mock_change_password_form.return_value.is_valid.assert_called_once_with()

    @patch("api.views.change_password_view.User")
    @patch("api.views.change_password_view.ChangePasswordForm")
    def test_change_password_view_post_request_form_valid(self, mock_change_password_form, mock_user):
        """
        @patch("api.views.change_password_view.User")
        @patch("api.views.change_password_view.ChangePasswordForm")
        def test_change_password_view_post_request_form_valid(self, mock_change_password_form, mock_user)
        """

        user = User(email=self.user_credentials["email"], password=self.user_credentials["password"])

        mock_change_password_form.return_value.is_valid.return_value = True
        mock_cleaned_data = PropertyMock(return_value=self.user_credentials)
        type(mock_change_password_form.return_value).cleaned_data = mock_cleaned_data
        mock_user.objects.get.return_value = user

        request = self.request_factory.post("/urban_development/change_password/")
        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_change_password_form.return_value.is_valid.assert_called_once_with()
        mock_cleaned_data.assert_called_once_with()
        mock_user.objects.get.assert_called_once_with(email=self.user_credentials["email"])
