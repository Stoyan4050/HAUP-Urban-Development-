"""
test_manual_classification_view.py
"""

import json
import unittest
from unittest.mock import patch
from django.test import RequestFactory
from api.views.manual_classification_view import ManualClassificationView


class TestManualClassificationView(unittest.TestCase):
    """
    class TestManualClassificationView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    def test_manual_classification_view_guest_user(self):
        """
        def test_manual_classification_view_guest_user(self)
        """

        parameters = {
            "classified_by": "guest",
        }

        request = self.request_factory.get("/urban_development/manual_classification/")
        response = ManualClassificationView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(json.loads(response.content))

    @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
    @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
    @patch("api.views.manual_classification_view.manual_classify")
    def test_manual_classification_view_contains_greenery_false(self,
                                                                mock_manual_classify,
                                                                mock_tile_to_coordinates,
                                                                mock_coordinates_to_tile):
        """
        @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
        @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
        @patch("api.views.manual_classification_view.manual_classify")
        def test_manual_classification_view_contains_greenery_false(self,
                                                                    mock_manual_classify,
                                                                    mock_tile_to_coordinates,
                                                                    mock_coordinates_to_tile)
        """

        parameters = {
            "classified_by": "user",
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "contains_greenery": "False",
            "greenery_amount": "unknown",
        }
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_manual_classify.return_value = None
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/manual_classification/")
        response = ManualClassificationView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": parameters["longitude"],
            "y_coordinate": parameters["latitude"],
            "contains_greenery": parameters["contains_greenery"].lower(),
            "greenery_amount": parameters["greenery_amount"],
        })
        mock_manual_classify.assert_called_once_with(parameters["longitude"], parameters["latitude"],
                                                     parameters["year"], parameters["classified_by"],
                                                     0, parameters["contains_greenery"])
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
    @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
    @patch("api.views.manual_classification_view.manual_classify")
    def test_manual_classification_view_greenery_amount_low(self,
                                                            mock_manual_classify,
                                                            mock_tile_to_coordinates,
                                                            mock_coordinates_to_tile):
        """
        @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
        @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
        @patch("api.views.manual_classification_view.manual_classify")
        def test_manual_classification_view_greenery_amount_low(self,
                                                                mock_manual_classify,
                                                                mock_tile_to_coordinates,
                                                                mock_coordinates_to_tile)
        """

        parameters = {
            "classified_by": "user",
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "contains_greenery": "True",
            "greenery_amount": "low",
        }
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_manual_classify.return_value = None
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/manual_classification/")
        response = ManualClassificationView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": parameters["longitude"],
            "y_coordinate": parameters["latitude"],
            "contains_greenery": parameters["contains_greenery"].lower(),
            "greenery_amount": parameters["greenery_amount"],
        })
        mock_manual_classify.assert_called_once_with(parameters["longitude"], parameters["latitude"],
                                                     parameters["year"], parameters["classified_by"],
                                                     0.165, parameters["contains_greenery"])
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
    @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
    @patch("api.views.manual_classification_view.manual_classify")
    def test_manual_classification_view_greenery_amount_medium(self,
                                                               mock_manual_classify,
                                                               mock_tile_to_coordinates,
                                                               mock_coordinates_to_tile):
        """
        @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
        @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
        @patch("api.views.manual_classification_view.manual_classify")
        def test_manual_classification_view_greenery_amount_medium(self,
                                                                   mock_manual_classify,
                                                                   mock_tile_to_coordinates,
                                                                   mock_coordinates_to_tile)
        """

        parameters = {
            "classified_by": "user",
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "contains_greenery": "True",
            "greenery_amount": "medium",
        }
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_manual_classify.return_value = None
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/manual_classification/")
        response = ManualClassificationView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": parameters["longitude"],
            "y_coordinate": parameters["latitude"],
            "contains_greenery": parameters["contains_greenery"].lower(),
            "greenery_amount": parameters["greenery_amount"],
        })
        mock_manual_classify.assert_called_once_with(parameters["longitude"], parameters["latitude"],
                                                     parameters["year"], parameters["classified_by"],
                                                     0.445, parameters["contains_greenery"])
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
    @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
    @patch("api.views.manual_classification_view.manual_classify")
    def test_manual_classification_view_greenery_amount_high(self,
                                                             mock_manual_classify,
                                                             mock_tile_to_coordinates,
                                                             mock_coordinates_to_tile):
        """
        @patch("api.views.manual_classification_view.transform_coordinates_to_tile")
        @patch("api.views.manual_classification_view.transform_tile_to_coordinates")
        @patch("api.views.manual_classification_view.manual_classify")
        def test_manual_classification_view_greenery_amount_high(self,
                                                                 mock_manual_classify,
                                                                 mock_tile_to_coordinates,
                                                                 mock_coordinates_to_tile)
        """

        parameters = {
            "classified_by": "user",
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "contains_greenery": "True",
            "greenery_amount": "high",
        }
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_manual_classify.return_value = None
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/manual_classification/")
        response = ManualClassificationView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": parameters["longitude"],
            "y_coordinate": parameters["latitude"],
            "contains_greenery": parameters["contains_greenery"].lower(),
            "greenery_amount": parameters["greenery_amount"],
        })
        mock_manual_classify.assert_called_once_with(parameters["longitude"], parameters["latitude"],
                                                     parameters["year"], parameters["classified_by"],
                                                     0.83, parameters["contains_greenery"])
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
