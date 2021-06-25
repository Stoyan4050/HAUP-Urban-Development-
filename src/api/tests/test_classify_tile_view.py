"""
test_classify_tile_view.py
"""

import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from api.views.classify_tile_view import ClassifyTileView


class TestClassifyTileView(unittest.TestCase):
    """
    class TestClassifyTileView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    def test_classsify_tile_view_guest_user(self):
        """
        def test_classsify_tile_view_guest_user(self)
        """

        parameters = {
            "user": "guest"
        }

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(json.loads(response.content))

    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_tile_not_classified(self, mock_coordinates_to_tile, mock_classify_cnn):
        """
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_tile_not_classified(self, mock_coordinates_to_tile, mock_classify_cnn)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = None

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(json.loads(response.content))
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_contains_greenery_unknown(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                           mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_contains_greenery_unknown(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                               mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": "unknown",
            "greenery_percentage": "unknown",
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "unknown",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_contains_greenery_false(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                         mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_contains_greenery_false(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                             mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": False,
            "greenery_percentage": "unknown",
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "none",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_greenery_amount_low(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                     mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_greenery_amount_low(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                         mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": True,
            "greenery_percentage": 0.165,
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "low",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_greenery_amount_medium(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                        mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_greenery_amount_medium(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                            mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": True,
            "greenery_percentage": 0.445,
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "medium",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_greenery_amount_high(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                      mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_greenery_amount_high(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                          mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": True,
            "greenery_percentage": 0.83,
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "high",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])

    @patch("api.views.classify_tile_view.Transformer")
    @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
    @patch("api.views.classify_tile_view.classify_cnn")
    @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
    def test_classsify_tile_view_greenery_amount_incorrect(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                           mock_tile_to_coordinates, mock_transformer):
        """
        @patch("api.views.classify_tile_view.Transformer")
        @patch("api.views.classify_tile_view.transform_tile_to_coordinates")
        @patch("api.views.classify_tile_view.classify_cnn")
        @patch("api.views.classify_tile_view.transform_coordinates_to_tile")
        def test_classsify_tile_view_greenery_amount_incorrect(self, mock_coordinates_to_tile, mock_classify_cnn,
                                                               mock_tile_to_coordinates, mock_transformer)
        """

        parameters = {
            "longitude": 1,
            "latitude": 2,
            "year": 3,
            "user": "user",
        }
        coordinates_to_tile = 11, 12
        classify_cnn = {
            "contains_greenery": True,
            "greenery_percentage": -1,
        }
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        transformer = 50, 60

        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_classify_cnn.return_value = classify_cnn
        mock_tile_to_coordinates.return_value = tile_to_coordinates
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)

        request = self.request_factory.get("/urban_development/classify_tile/")
        response = ClassifyTileView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "contains_greenery": classify_cnn["contains_greenery"],
            "greenery_amount": "unknown",
        })
        mock_coordinates_to_tile.assert_called_once_with(parameters["longitude"], parameters["latitude"])
        mock_classify_cnn.assert_called_once_with(parameters["year"],
                                                  coordinates_to_tile[0] * 75879 + coordinates_to_tile[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])
