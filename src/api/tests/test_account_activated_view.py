"""
test_account_activated_view.py
"""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from api.models.user import User
from api.views.account_activated_view import AccountActivatedView


class TestAccountActivatedView(unittest.TestCase):
    """
    class TestAccountActivatedView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user_credentials = {
            "username": "username",
            "password": "password",
        }
        self.uidb64 = "uidb64"
        self.token = "token"
        self.request_factory = RequestFactory()

    @patch("api.views.account_activated_view.User")
    @patch("api.views.account_activated_view.force_text")
    @patch("api.views.account_activated_view.urlsafe_base64_decode")
    def test_send_activation_email_view_user_error(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.account_activated_view.User")
        @patch("api.views.account_activated_view.force_text")
        @patch("api.views.account_activated_view.urlsafe_base64_decode")
        def test_send_activation_email_view_user_error(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get = MagicMock(side_effect=ObjectDoesNotExist("Exception."))

        request = self.request_factory.get("/urban_development/account_activated/")
        response = AccountActivatedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.account_activated_view.User")
    @patch("api.views.account_activated_view.force_text")
    @patch("api.views.account_activated_view.urlsafe_base64_decode")
    def test_send_activation_email_view_user_none(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.account_activated_view.User")
        @patch("api.views.account_activated_view.force_text")
        @patch("api.views.account_activated_view.urlsafe_base64_decode")
        def test_send_activation_email_view_user_none(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = None

        request = self.request_factory.get("/urban_development/account_activated/")
        response = AccountActivatedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.account_activated_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.account_activated_view.User")
    @patch("api.views.account_activated_view.force_text")
    @patch("api.views.account_activated_view.urlsafe_base64_decode")
    def test_send_activation_email_view_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                 mock_user, mock_check_token):
        """
        @patch("api.views.account_activated_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.account_activated_view.User")
        @patch("api.views.account_activated_view.force_text")
        @patch("api.views.account_activated_view.urlsafe_base64_decode")
        def test_send_activation_email_view_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                     mock_user, mock_check_token)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = False

        request = self.request_factory.get("/urban_development/account_activated/")
        response = AccountActivatedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)

    @patch("api.views.account_activated_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.account_activated_view.User")
    @patch("api.views.account_activated_view.force_text")
    @patch("api.views.account_activated_view.urlsafe_base64_decode")
    def test_send_activation_email_view_user_valid_token_valid(self, mock_decode, mock_force_text,
                                                               mock_user, mock_check_token):
        """
        @patch("api.views.account_activated_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.account_activated_view.User")
        @patch("api.views.account_activated_view.force_text")
        @patch("api.views.account_activated_view.urlsafe_base64_decode")
        def test_send_activation_email_view_user_valid_token_valid(self, mock_decode, mock_force_text,
                                                                   mock_user, mock_check_token)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])
        user.save = MagicMock(return_value=None)

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = True

        request = self.request_factory.get("/urban_development/account_activated/")
        response = AccountActivatedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)
        user.save.assert_called_once_with()
