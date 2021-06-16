"""
tests.py
"""

from django.test import SimpleTestCase
from django.core.exceptions import ObjectDoesNotExist

from classification.classifier import get_image_from_url, find_color_image


class GetImageFromUrl(SimpleTestCase):
    """
    get tile images from url tests class
    """

    def test_http_error(self):
        """
        def test_http_error
        """
        image = get_image_from_url(2020, 0, 0)
        self.assertEqual(None, image)

    def test_get_image(self):
        """
        def test_get_image
        """
        image = get_image_from_url(2020, 75111, 75659)
        self.assertIsNotNone(image)


class ColorDetectionTest(SimpleTestCase):
    """
    color detection tests class
    """

    # tests have been created by manually checking the approximate percentage of green on a tile
    def test_no_green(self):
        """
        tests a tile containing no green
        """
        image_percentage = find_color_image(75418, 75317, 2020)
        self.assertTrue(image_percentage * 100 < 0.1)
        self.assertEqual(0.0006256103515625, image_percentage)

    def test_minimal_green(self):
        """
        tests a tile with bare minimum green
        """
        image_percentage = find_color_image(75505, 75546, 2020)
        self.assertTrue(image_percentage * 100 > 0.5)
        self.assertTrue(image_percentage * 100 < 1)
        self.assertEqual(0.005366007486979167, image_percentage)

    def test_minimal_green_two(self):
        """
        tests a tile with bare minimum green
        """
        image_percentage = find_color_image(75507, 75546, 2020)
        self.assertTrue(image_percentage * 100 > 0.5)
        self.assertTrue(image_percentage * 100 < 1)
        self.assertEqual(0.006261189778645833, image_percentage)

    def test_ten_green(self):
        """
        tests a tile with approximately 10% green
        """
        image_percentage = find_color_image(75650, 75202, 2020)
        self.assertTrue(image_percentage * 100 > 8)
        self.assertTrue(image_percentage * 100 < 12)
        self.assertEqual(0.094512939453125, image_percentage)

    def test_fifteen_green(self):
        """
        tests a tile with approximately 15% green
        """
        image_percentage = find_color_image(75202, 75593, 2020)
        self.assertTrue(image_percentage * 100 > 15)
        self.assertTrue(image_percentage * 100 < 20)
        self.assertEqual(0.15974934895833334, image_percentage)

    def test_thirty_green(self):
        """
        tests a tile with approximately 30% green
        """
        image_percentage = find_color_image(75509, 75553, 2020)
        self.assertTrue(image_percentage * 100 > 30)
        self.assertTrue(image_percentage * 100 < 35)
        self.assertEqual(0.32403564453125, image_percentage)

    def test_forty_green(self):
        """
        tests a tile with approximately 40% green
        """
        image_percentage = find_color_image(75506, 75552, 2020)
        self.assertTrue(image_percentage * 100 > 40)
        self.assertTrue(image_percentage * 100 < 45)
        self.assertEqual(0.4395802815755208, image_percentage)

    def test_fifty_green(self):
        """
        tests a tile with approximately 50% green
        """
        image_percentage = find_color_image(75449, 75543, 2020)
        self.assertTrue(image_percentage * 100 > 49)
        self.assertTrue(image_percentage * 100 < 52)
        self.assertEqual(0.5019989013671875, image_percentage)

    def test_sixty_green(self):
        """
        tests a tile with approximately 60% green
        """
        image_percentage = find_color_image(75511, 75553, 2020)
        self.assertTrue(image_percentage * 100 > 60)
        self.assertTrue(image_percentage * 100 < 65)
        self.assertEqual(0.6011098225911459, image_percentage)

    def test_almost_full_green(self):
        """
        tests a tile containing mainly green
        """
        image_percentage = find_color_image(75515, 75551, 2020)
        self.assertTrue(image_percentage * 100 > 80)
        self.assertEqual(0.8185831705729166, image_percentage)

    def test_full_green(self):
        """
        tests a tile containing primarily only green
        """
        image_percentage = find_color_image(75416, 75550, 2020)
        self.assertTrue(image_percentage * 100 > 80)
        self.assertEqual(0.8505350748697916, image_percentage)

    def test_farm_land_no_greenery(self):
        """
        tests that farmland is not detected as greenery due to boundaries
        """
        image_percentage = find_color_image(75507, 75330, 2020)
        self.assertTrue(image_percentage * 100 < 0.5)
        self.assertEqual(0.0022684733072916665, image_percentage)

    def test_image_not_found(self):
        """
        tests that non-existed tile throws an exception
        """
        with self.assertRaises(ObjectDoesNotExist):
            find_color_image(0, 0, 2020)
