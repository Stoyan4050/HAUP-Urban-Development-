"""
test_register_view.py
"""

import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from api.models.user import User
from api.views.register_view import RegisterView


class TestRegisterView(unittest.TestCase):
    """
    class TestRegisterView(unittest.TestCase)
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

    def test_register_view_get_request(self):
        """
        def test_register_view_get_request(self)
        """

        request = self.request_factory.get("/urban_development/register/")
        response = RegisterView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    @patch("api.views.register_view.RegisterForm")
    def test_register_view_post_request_form_invalid(self, mock_register_form):
        """
        @patch("api.views.register_view.RegisterForm")
        def test_register_view_post_request_form_invalid(self, mock_register_form)
        """

        mock_register_form.return_value.is_valid.return_value = False

        request = self.request_factory.post("/urban_development/register/")
        response = RegisterView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        mock_register_form.return_value.is_valid.assert_called_once_with()

    @patch("api.views.register_view.RegisterForm")
    def test_register_view_post_request_form_valid(self, mock_register_form):
        """
        @patch("api.views.register_view.RegisterForm")
        def test_register_view_post_request_form_valid(self, mock_register_form)
        """

        user = User(email=self.user_credentials["username"], password=self.user_credentials["password"])
        user.save = MagicMock(return_value=None)

        mock_register_form.return_value.is_valid.return_value = True
        mock_register_form.return_value.save.return_value = user

        request = self.request_factory.post("/urban_development/register/")
        response = RegisterView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_register_form.return_value.is_valid.assert_called_once_with()
        mock_register_form.return_value.save.assert_called_once_with(commit=False)
        user.save.assert_called_once_with()
