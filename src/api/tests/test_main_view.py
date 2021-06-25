"""
test_main_view.py
"""

import unittest
from django.test import RequestFactory
from api.views.main_view import MainView


class TestMainView(unittest.TestCase):
    """
    class TestMainView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    def test_main_view_get_request(self):
        """
        def test_main_view_get_request(self)
        """

        request = self.request_factory.get("/urban_development/main/")
        response = MainView.as_view()(request)

        self.assertEqual(response.status_code, 200)
