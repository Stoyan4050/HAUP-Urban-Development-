"""
test_base_view.py
"""

import unittest
from unittest.mock import PropertyMock
from django.test import RequestFactory
from api.models.user import User
from api.views.base_view import BaseView


class TestBaseView(unittest.TestCase):
    """
    class TestBaseView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.user = User(email="email", password="password")
        self.request_factory = RequestFactory()

    def test_base_view_not_authenticated(self):
        """
        def test_base_view_not_authenticated(self)
        """

        mock_is_authenticated = PropertyMock(return_value=False)
        type(self.user).is_authenticated = mock_is_authenticated

        request = self.request_factory.get("/urban_development/base/")
        request.user = self.user
        response = BaseView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_is_authenticated.assert_called_once_with()

    def test_base_view_authenticated(self):
        """
        def test_base_view_authenticated(self):
        """

        mock_is_authenticated = PropertyMock(return_value=True)
        type(self.user).is_authenticated = mock_is_authenticated

        request = self.request_factory.get("/urban_development/base/")
        request.user = self.user
        response = BaseView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        mock_is_authenticated.assert_called_once_with()
