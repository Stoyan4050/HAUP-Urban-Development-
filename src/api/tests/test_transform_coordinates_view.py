"""
test_transform_coordinates_view.py
"""

import json
from math import floor
import unittest
from unittest.mock import call, patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from api.models.classification import Classification
from api.models.tile import Tile
from api.views.transform_coordinates_view import TransformCoordinatesView


class TestTransformCoordinatesView(unittest.TestCase):
    """
    class TestTransformCoordinatesView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_no_classifications(self, mock_classification, mock_transformer,
                                                           mock_coordinates_to_tile, mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_no_classifications(self, mock_classification, mock_transformer,
                                                               mock_coordinates_to_tile, mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        mock_query_set.filter.return_value.values.return_value = list()
        mock_query_set.get = MagicMock(side_effect=ObjectDoesNotExist("Exception."))
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "unknown",
            "contains_greenery": "unknown",
            "greenery_amount": "unknown",
            "year": "unknown",
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=-1)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_one_classification_classifier(self,
                                                                      mock_classification,
                                                                      mock_transformer,
                                                                      mock_coordinates_to_tile,
                                                                      mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_one_classification_classifier(self,
                                                                          mock_classification,
                                                                          mock_transformer,
                                                                          mock_coordinates_to_tile,
                                                                          mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classifications = (
            {
                "tile": tile,
                "year": 2005,
                "contains_greenery": True,
                "greenery_percentage": 0.165,
                "classified_by": -1,
            },
        )
        classification = Classification(tile=classifications[0]["tile"],
                                        year=classifications[0]["year"],
                                        contains_greenery=classifications[0]["contains_greenery"],
                                        greenery_percentage=classifications[0]["greenery_percentage"],
                                        classified_by=classifications[0]["classified_by"])
        mock_query_set.filter.return_value.values.return_value = [classification.__dict__]
        mock_query_set.get.return_value = classification
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "classifier",
            "contains_greenery": True,
            "greenery_amount": "low",
            "year": 2005,
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=2005)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_one_classification_training_data(self,
                                                                         mock_classification,
                                                                         mock_transformer,
                                                                         mock_coordinates_to_tile,
                                                                         mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_one_classification_training_data(self,
                                                                             mock_classification,
                                                                             mock_transformer,
                                                                             mock_coordinates_to_tile,
                                                                             mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classifications = (
            {
                "tile": tile,
                "year": 1900,
                "contains_greenery": True,
                "greenery_percentage": 0.445,
                "classified_by": -2,
            },
        )
        classification = Classification(tile=classifications[0]["tile"],
                                        year=classifications[0]["year"],
                                        contains_greenery=classifications[0]["contains_greenery"],
                                        greenery_percentage=classifications[0]["greenery_percentage"],
                                        classified_by=classifications[0]["classified_by"])
        mock_query_set.filter.return_value.values.return_value = [classification.__dict__]
        mock_query_set.get.return_value = classification
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "training data",
            "contains_greenery": True,
            "greenery_amount": "medium",
            "year": 1900,
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=1900)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_one_classification_user(self,
                                                                mock_classification,
                                                                mock_transformer,
                                                                mock_coordinates_to_tile,
                                                                mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_one_classification_user(self,
                                                                    mock_classification,
                                                                    mock_transformer,
                                                                    mock_coordinates_to_tile,
                                                                    mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classifications = (
            {
                "tile": tile,
                "year": 2021,
                "contains_greenery": True,
                "greenery_percentage": 0.83,
                "classified_by": 1,
            },
        )
        classification = Classification(tile=classifications[0]["tile"],
                                        year=classifications[0]["year"],
                                        contains_greenery=classifications[0]["contains_greenery"],
                                        greenery_percentage=classifications[0]["greenery_percentage"],
                                        classified_by=classifications[0]["classified_by"])
        mock_query_set.filter.return_value.values.return_value = [classification.__dict__]
        mock_query_set.get.return_value = classification
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "user",
            "contains_greenery": True,
            "greenery_amount": "high",
            "year": 2021,
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=2021)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_many_classifications_unknown_greenery(self,
                                                                              mock_classification,
                                                                              mock_transformer,
                                                                              mock_coordinates_to_tile,
                                                                              mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_many_classifications_unknown_greenery(self,
                                                                                  mock_classification,
                                                                                  mock_transformer,
                                                                                  mock_coordinates_to_tile,
                                                                                  mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classifications = (
            {
                "tile": tile,
                "year": 2015,
                "contains_greenery": True,
                "greenery_percentage": -1,
                "classified_by": 0,
            },
            {
                "tile": tile,
                "year": 2000,
                "contains_greenery": False,
                "greenery_percentage": 0,
                "classified_by": -2,
            },
        )
        classification_1 = Classification(tile=classifications[0]["tile"],
                                          year=classifications[0]["year"],
                                          contains_greenery=classifications[0]["contains_greenery"],
                                          greenery_percentage=classifications[0]["greenery_percentage"],
                                          classified_by=classifications[0]["classified_by"])
        classification_2 = Classification(tile=classifications[1]["tile"],
                                          year=classifications[1]["year"],
                                          contains_greenery=classifications[1]["contains_greenery"],
                                          greenery_percentage=classifications[1]["greenery_percentage"],
                                          classified_by=classifications[1]["classified_by"])
        mock_query_set.filter.return_value.values.return_value = [classification_1.__dict__,
                                                                  classification_2.__dict__]
        mock_query_set.get.return_value = classification_1
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "unknown",
            "contains_greenery": True,
            "greenery_amount": "unknown",
            "year": 2015,
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=2015)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])

    @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
    @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
    @patch("api.views.transform_coordinates_view.Transformer")
    @patch("api.views.transform_coordinates_view.Classification")
    def test_transform_coordinates_view_many_classifications_no_greenery(self,
                                                                         mock_classification,
                                                                         mock_transformer,
                                                                         mock_coordinates_to_tile,
                                                                         mock_tile_to_coordinates):
        """
        @patch("api.views.transform_coordinates_view.transform_tile_to_coordinates")
        @patch("api.views.transform_coordinates_view.transform_coordinates_to_tile")
        @patch("api.views.transform_coordinates_view.Transformer")
        @patch("api.views.transform_coordinates_view.Classification")
        def test_transform_coordinates_view_many_classifications_no_greenery(self,
                                                                             mock_classification,
                                                                             mock_transformer,
                                                                             mock_coordinates_to_tile,
                                                                             mock_tile_to_coordinates)
        """

        parameters = {
            "x_coordinate": 1,
            "y_coordinate": 2,
            "year": 3,
        }
        transformer = 50, 60
        coordinates_to_tile = 11, 12
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classifications = (
            {
                "tile": tile,
                "year": 1950,
                "contains_greenery": True,
                "greenery_percentage": -1,
                "classified_by": 0,
            },
            {
                "tile": tile,
                "year": 1975,
                "contains_greenery": False,
                "greenery_percentage": 0,
                "classified_by": -2,
            },
        )
        classification_1 = Classification(tile=classifications[0]["tile"],
                                          year=classifications[0]["year"],
                                          contains_greenery=classifications[0]["contains_greenery"],
                                          greenery_percentage=classifications[0]["greenery_percentage"],
                                          classified_by=classifications[0]["classified_by"])
        classification_2 = Classification(tile=classifications[1]["tile"],
                                          year=classifications[1]["year"],
                                          contains_greenery=classifications[1]["contains_greenery"],
                                          greenery_percentage=classifications[1]["greenery_percentage"],
                                          classified_by=classifications[1]["classified_by"])
        mock_query_set.filter.return_value.values.return_value = [classification_1.__dict__,
                                                                  classification_2.__dict__]
        mock_query_set.get.return_value = classification_2
        mock_classification.objects = mock_query_set
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_coordinates_to_tile.return_value = coordinates_to_tile
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/transform_coordinates/")
        response = TransformCoordinatesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        x_tile = floor((parameters["x_coordinate"] - 13328.546) / 406.40102300613496932515337423313) + 75120
        y_tile = floor((619342.658 - parameters["y_coordinate"]) / 406.40607802340702210663198959688) + 75032
        tile_id = x_tile * 75879 + y_tile
        self.assertEqual(json.loads(response.content), {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": tile_to_coordinates["xmin"],
            "ymin": tile_to_coordinates["ymin"],
            "xmax": tile_to_coordinates["xmax"],
            "ymax": tile_to_coordinates["ymax"],
            "x_coordinate": transformer[0],
            "y_coordinate": transformer[1],
            "classified_by": "training data",
            "contains_greenery": False,
            "greenery_amount": "none",
            "year": 1975,
        })
        mock_classification.objects.filter.assert_called_once_with(tile=tile_id, year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with()
        mock_classification.objects.get.assert_called_once_with(tile=tile_id, year=1975)
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(parameters["x_coordinate"],
                                                                                parameters["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_coordinates_to_tile.assert_called_once_with(transformer[0], transformer[1])
        mock_tile_to_coordinates.assert_called_once_with(coordinates_to_tile[0], coordinates_to_tile[1])
