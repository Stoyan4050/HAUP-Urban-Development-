"""
test_login_view.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from django.test import RequestFactory
from api.models.user import User
from api.views.login_view import LoginView


class TestLoginView(unittest.TestCase):
    """
    class TestLoginView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user_credentials = {
            "username": "username",
            "password": "password",
        }
        self.request_factory = RequestFactory()

    def test_login_view_get_request(self):
        """
        def test_login_view_get_request(self)
        """

        request = self.request_factory.get("/urban_development/login/")
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    @patch("api.views.login_view.LoginForm")
    def test_login_view_post_request_form_invalid(self, mock_login_form):
        """
        @patch("api.views.login_view.LoginForm")
        def test_login_view_post_request_form_invalid(self, mock_login_form)
        """

        mock_login_form.return_value.is_valid.return_value = False

        request = self.request_factory.post("/urban_development/login/")
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        mock_login_form.return_value.is_valid.assert_called_once_with()

    @patch("api.views.login_view.authenticate")
    @patch("api.views.login_view.LoginForm")
    def test_login_view_post_request_user_none(self, mock_login_form, mock_authenticate):
        """
        @patch("api.views.login_view.authenticate")
        @patch("api.views.login_view.LoginForm")
        def test_login_view_post_request_user_none(self, mock_login_form, mock_authenticate)
        """

        mock_login_form.return_value.is_valid.return_value = True
        mock_cleaned_data = PropertyMock(return_value=self.user_credentials)
        type(mock_login_form.return_value).cleaned_data = mock_cleaned_data
        mock_authenticate.return_value = None

        request = self.request_factory.post("/urban_development/login/")
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        mock_login_form.return_value.is_valid.assert_called_once_with()
        mock_cleaned_data.assert_called_once_with()
        mock_authenticate.assert_called_once_with(request,
                                                  username=self.user_credentials["username"],
                                                  password=self.user_credentials["password"])

    @patch("api.views.login_view.login")
    @patch("api.views.login_view.authenticate")
    @patch("api.views.login_view.LoginForm")
    def test_login_view_post_request_user_valid(self, mock_login_form, mock_authenticate, mock_login):
        """
        @patch("api.views.login_view.login")
        @patch("api.views.login_view.authenticate")
        @patch("api.views.login_view.LoginForm")
        def test_login_view_post_request_user_valid(self, mock_login_form, mock_authenticate, mock_login)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])

        mock_login_form.return_value.is_valid.return_value = True
        mock_cleaned_data = PropertyMock(return_value=self.user_credentials)
        type(mock_login_form.return_value).cleaned_data = mock_cleaned_data
        mock_authenticate.return_value = user
        mock_login.return_value = None

        request = self.request_factory.post("/urban_development/login/")
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_login_form.return_value.is_valid.assert_called_once_with()
        mock_cleaned_data.assert_called_once_with()
        mock_authenticate.assert_called_once_with(request,
                                                  username=self.user_credentials["username"],
                                                  password=self.user_credentials["password"])
        mock_login.assert_called_once_with(request, user)
