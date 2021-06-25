"""
test_guest_view.py
"""

import unittest
from unittest.mock import patch
from django.test import RequestFactory
from api.views.guest_view import GuestView


class TestGuestView(unittest.TestCase):
    """
    class TestGuestView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    @patch("api.views.guest_view.logout")
    def test_guest_view(self, mock_logout):
        """
        @patch("api.views.guest_view.logout")
        def test_guest_view(self, mock_logout)
        """

        mock_logout.return_value = None

        request = self.request_factory.get("/urban_development/guest/")
        response = GuestView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_logout.assert_called_once_with(request)
