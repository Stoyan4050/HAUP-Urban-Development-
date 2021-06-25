"""
test_send_change_password_email_view.py
"""

import unittest
from unittest.mock import patch
from django.contrib.sites.shortcuts import get_current_site
from django.test import RequestFactory
from api.views.send_change_password_email_view import SendChangePasswordEmailView


class TestSendChangePasswordEmailView(unittest.TestCase):
    """
    class TestSendChangePasswordEmailView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.uid = "1"
        self.request_factory = RequestFactory()

    @patch("api.views.send_change_password_email_view.send_email")
    def test_send_change_password_email_view_failure(self, mock_send_email):
        """
        @patch("api.views.send_change_password_email_view.send_email")
        def test_send_change_password_email_view_failure(self, mock_send_email)
        """

        mock_send_email.return_value = False

        request = self.request_factory.get("/urban_development/send_change_password_email/")
        response = SendChangePasswordEmailView.as_view()(request, self.uid)

        self.assertEqual(response.status_code, 200)
        mock_send_email.assert_called_once_with(self.uid,
                                                get_current_site(request).domain,
                                                "Change the password for your Urban Development account.",
                                                "pages/change_password_email.html")

    @patch("api.views.send_change_password_email_view.send_email")
    def test_send_change_password_email_view_success(self, mock_send_email):
        """
        @patch("api.views.send_change_password_email_view.send_email")
        def test_send_change_password_email_view_success(self, mock_send_email)
        """

        mock_send_email.return_value = True

        request = self.request_factory.get("/urban_development/send_change_password_email/")
        response = SendChangePasswordEmailView.as_view()(request, self.uid)

        self.assertEqual(response.status_code, 200)
        mock_send_email.assert_called_once_with(self.uid,
                                                get_current_site(request).domain,
                                                "Change the password for your Urban Development account.",
                                                "pages/change_password_email.html")
