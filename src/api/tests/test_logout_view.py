"""
test_logout_view.py
"""

import unittest
from unittest.mock import patch
from django.test import RequestFactory
from api.views.logout_view import LogoutView


class TestLogoutView(unittest.TestCase):
    """
    class TestLogoutView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    @patch("api.views.logout_view.logout")
    def test_logout_view(self, mock_logout):
        """
        @patch("api.views.logout_view.logout")
        def test_logout_view(self, mock_logout)
        """

        mock_logout.return_value = None

        request = self.request_factory.get("/urban_development/logout/")
        response = LogoutView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_logout.assert_called_once_with(request)
