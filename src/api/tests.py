"""
tests.py
"""

from django.test import SimpleTestCase

from api.classifier import get_image_from_url, color_detection


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
        def test_no_green
        """
        image_percentage = color_detection(75418, 75317, 2020)
        self.assertTrue(image_percentage * 100 < 0.1)
        self.assertEqual(0.0006256103515625, image_percentage)

    def test_minimal_green(self):
        """
        def test_minimal_green
        """
        image_percentage = color_detection(75505, 75546, 2020)
        self.assertTrue(image_percentage * 100 > 0.5)
        self.assertTrue(image_percentage * 100 < 1)
        self.assertEqual(0.005366007486979167, image_percentage)

    def test_minimal_green_two(self):
        """
        def test_minimal_green_two
        """
        image_percentage = color_detection(75507, 75546, 2020)
        self.assertTrue(image_percentage * 100 > 0.5)
        self.assertTrue(image_percentage * 100 < 1)
        self.assertEqual(0.006261189778645833, image_percentage)

    def test_ten_green(self):
        """
        def test_ten_green
        """
        image_percentage = color_detection(75650, 75202, 2020)
        self.assertTrue(image_percentage * 100 > 8)
        self.assertTrue(image_percentage * 100 < 12)
        self.assertEqual(0.094512939453125, image_percentage)

    def test_fifteen_green(self):
        """
        def test_fifteen_green
        """
        image_percentage = color_detection(75202, 75593, 2020)
        self.assertTrue(image_percentage * 100 > 15)
        self.assertTrue(image_percentage * 100 < 20)
        self.assertEqual(0.15974934895833334, image_percentage)

    def test_thirty_green(self):
        """
        def test_thirty_green
        """
        image_percentage = color_detection(75509, 75553, 2020)
        self.assertTrue(image_percentage * 100 > 30)
        self.assertTrue(image_percentage * 100 < 35)
        self.assertEqual(0.32403564453125, image_percentage)

    def test_forty_green(self):
        """
        def test_forty_green
        """
        image_percentage = color_detection(75506, 75552, 2020)
        self.assertTrue(image_percentage * 100 > 40)
        self.assertTrue(image_percentage * 100 < 45)
        self.assertEqual(0.4395802815755208, image_percentage)

    def test_fifty_green(self):
        """
        def test_fifty_green
        """
        image_percentage = color_detection(75449, 75543, 2020)
        self.assertTrue(image_percentage * 100 > 49)
        self.assertTrue(image_percentage * 100 < 52)
        self.assertEqual(0.5019989013671875, image_percentage)

    def test_sixty_green(self):
        """
        def test_sixty_green
        """
        image_percentage = color_detection(75511, 75553, 2020)
        self.assertTrue(image_percentage * 100 > 60)
        self.assertTrue(image_percentage * 100 < 65)
        self.assertEqual(0.6011098225911459, image_percentage)

    def test_almost_full_green(self):
        """
        def test_almost_full_green
        """
        image_percentage = color_detection(75515, 75551, 2020)
        self.assertTrue(image_percentage * 100 > 80)
        self.assertEqual(0.8185831705729166, image_percentage)

    def test_full_green(self):
        """
        def test_full_green
        """
        image_percentage = color_detection(75416, 75550, 2020)
        self.assertTrue(image_percentage * 100 > 80)
        self.assertEqual(0.8505350748697916, image_percentage)

    def test_farm_land_no_greenery(self):
        """
        def test_farm_land_no_greenery
        """
        image_percentage = color_detection(75507, 75330, 2020)
        self.assertTrue(image_percentage * 100 < 0.5)
        self.assertEqual(0.0022684733072916665, image_percentage)
