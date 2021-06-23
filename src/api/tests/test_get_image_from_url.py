"""
test_get_image_from_url.py
"""

import unittest
from classification.classifier import get_image_from_url


class TestGetImageFromUrl(unittest.TestCase):
    """
    class TestGetImageFromUrl(unittest.TestCase)
    """

    def test_http_error(self):
        """
        def test_http_error(self)
        """

        image = get_image_from_url(2020, 0, 0)
        self.assertEqual(None, image)

    def test_get_image(self):
        """
        def test_get_image(self)
        """

        image = get_image_from_url(2020, 75111, 75659)
        self.assertIsNotNone(image)
