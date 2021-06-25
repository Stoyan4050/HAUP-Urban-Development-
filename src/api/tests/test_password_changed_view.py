"""
test_password_changed_view.py
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from api.models.user import User
from api.views.password_changed_view import PasswordChangedView


class TestPasswordChangedView(unittest.TestCase):
    """
    class TestPasswordChangedView(unittest.TestCase)
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
        self.new_password = "new_password"
        self.request_factory = RequestFactory()

    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_get_request_user_error(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_get_request_user_error(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get = MagicMock(side_effect=ObjectDoesNotExist("Exception."))

        request = self.request_factory.get("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_get_request_user_none(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_get_request_user_none(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = None

        request = self.request_factory.get("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_get_request_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                        mock_user, mock_check_token):
        """
        @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_get_request_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                            mock_user, mock_check_token)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = False

        request = self.request_factory.get("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)

    @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_get_request_user_valid_token_valid(self, mock_decode, mock_force_text,
                                                                      mock_user, mock_check_token):
        """
        @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_get_request_user_valid_token_valid(self, mock_decode, mock_force_text,
                                                                          mock_user, mock_check_token)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = True

        request = self.request_factory.get("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)

    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_post_request_user_error(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_post_request_user_error(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get = MagicMock(side_effect=ObjectDoesNotExist("Exception."))

        request = self.request_factory.post("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_post_request_user_none(self, mock_decode, mock_force_text, mock_user):
        """
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_post_request_user_none(self, mock_decode, mock_force_text, mock_user)
        """

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = None

        request = self.request_factory.post("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)

    @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_post_request_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                         mock_user, mock_check_token):
        """
        @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_post_request_user_valid_token_invalid(self, mock_decode, mock_force_text,
                                                                             mock_user, mock_check_token)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = False

        request = self.request_factory.post("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)

    @patch("api.views.password_changed_view.NewPasswordForm")
    @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_post_request_user_valid_token_valid_form_invalid(self,
                                                                                    mock_decode,
                                                                                    mock_force_text,
                                                                                    mock_user,
                                                                                    mock_check_token,
                                                                                    mock_new_password_form):
        """
        @patch("api.views.password_changed_view.NewPasswordForm")
        @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_post_request_user_valid_token_valid_form_invalid(self,
                                                                                        mock_decode,
                                                                                        mock_force_text,
                                                                                        mock_user,
                                                                                        mock_check_token,
                                                                                        mock_new_password_form)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = True
        mock_new_password_form.return_value.is_valid.return_value = False

        request = self.request_factory.post("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)
        mock_new_password_form.return_value.is_valid.assert_called_once_with()

    @patch("api.views.password_changed_view.NewPasswordForm")
    @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
    @patch("api.views.password_changed_view.User")
    @patch("api.views.password_changed_view.force_text")
    @patch("api.views.password_changed_view.urlsafe_base64_decode")
    def test_password_changed_view_post_request_user_valid_token_valid_form_valid(self,
                                                                                  mock_decode,
                                                                                  mock_force_text,
                                                                                  mock_user,
                                                                                  mock_check_token,
                                                                                  mock_new_password_form):
        """
        @patch("api.views.password_changed_view.NewPasswordForm")
        @patch("api.views.password_changed_view.TOKEN_GENERATOR.check_token")
        @patch("api.views.password_changed_view.User")
        @patch("api.views.password_changed_view.force_text")
        @patch("api.views.password_changed_view.urlsafe_base64_decode")
        def test_password_changed_view_post_request_user_valid_token_valid_form_valid(self,
                                                                                      mock_decode,
                                                                                      mock_force_text,
                                                                                      mock_user,
                                                                                      mock_check_token,
                                                                                      mock_new_password_form)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])
        user.set_password = MagicMock(return_value=None)
        user.save = MagicMock(return_value=None)

        mock_decode.return_value = None
        mock_force_text.return_value = None
        mock_user.objects.get.return_value = user
        mock_check_token.return_value = True
        mock_new_password_form.return_value.is_valid.return_value = True
        mock_cleaned_data = PropertyMock(return_value={"new_password1": self.new_password})
        type(mock_new_password_form.return_value).cleaned_data = mock_cleaned_data

        request = self.request_factory.post("/urban_development/password_changed/")
        response = PasswordChangedView.as_view()(request, self.uidb64, self.token)

        self.assertEqual(response.status_code, 200)
        mock_decode.assert_called_once_with(self.uidb64)
        mock_force_text.assert_called_once_with(None)
        mock_user.objects.get.assert_called_once_with(pk=None)
        mock_check_token.assert_called_once_with(user, self.token)
        mock_new_password_form.return_value.is_valid.assert_called_once_with()
        mock_cleaned_data.assert_called_once_with()
        user.set_password.assert_called_once_with(self.new_password)
        user.save.assert_called_once_with()
