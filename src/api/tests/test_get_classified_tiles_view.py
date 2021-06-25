"""
test_get_classified_tiles_view.py
"""

import json
import unittest
from unittest.mock import call, patch, MagicMock
from django.test import RequestFactory
from api.models.tile import Tile
from api.models.classification import Classification
from api.views.get_classified_tiles_view import GetClassifiedTilesView


class TestGetClassifiedTilesView(unittest.TestCase):
    """
    class TestGetClassifiedTilesView(unittest.TestCase)
    """

    def setUp(self):
        """
        def setUp(self)
        """

        self.request_factory = RequestFactory()

    @patch("api.views.get_classified_tiles_view.Classification")
    def test_get_classified_tiles_no_classifications(self, mock_classification):
        """
        @patch("api.views.get_classified_tiles_view.Classification")
        def test_get_classified_tiles_no_classifications(self, mock_classification)
        """

        parameters = {
            "year": 2021,
            "province": "None",
        }

        mock_query_set = MagicMock(spec=Classification.objects)
        mock_query_set.filter.return_value = mock_query_set
        mock_query_set.filter.return_value.values.return_value = mock_query_set
        classifications = list()
        mock_query_set.filter.return_value.values.return_value.distinct.return_value = classifications
        mock_classification.objects = mock_query_set

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 400)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with("tile_id")
        mock_classification.objects.filter.return_value.values.return_value.distinct.assert_called_once_with()

    @patch("api.views.get_classified_tiles_view.Classification")
    @patch("api.views.get_classified_tiles_view.Tile")
    def test_get_classified_tiles_no_classifications_single_region(self, mock_tile, mock_classification):
        """
        @patch("api.views.get_classified_tiles_view.Classification")
        @patch("api.views.get_classified_tiles_view.Tile")
        def test_get_classified_tiles_no_classifications_single_region(self, mock_tile, mock_classification)
        """

        parameters = {
            "year": 2021,
            "province": "Zuid-Holland",
        }

        mock_query_set_tile = MagicMock(spec=Tile.objects)
        mock_query_set_tile.filter.return_value = mock_query_set_tile
        tiles = [Tile(tile_id=100, x_coordinate=200, y_coordinate=300)]
        mock_query_set_tile.filter.return_value.values_list.return_value = tiles
        mock_tile.objects = mock_query_set_tile
        mock_query_set_classification = MagicMock(spec=Classification.objects)
        mock_query_set_classification.filter.return_value = mock_query_set_classification
        classifications = list()
        mock_query_set_classification.filter.return_value.distinct.return_value = classifications
        mock_classification.objects = mock_query_set_classification

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 400)
        mock_tile.objects.filter.assert_called_once_with(x_coordinate__gte=75205, x_coordinate__lte=75408,
                                                         y_coordinate__gte=75368, y_coordinate__lte=75552)
        mock_tile.objects.filter.return_value.values_list.assert_called_once_with("tile_id", flat=True)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"], tile_id__in=tiles)
        mock_classification.objects.filter.return_value.distinct.assert_called_once_with()

    @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
    @patch("api.views.get_classified_tiles_view.Transformer")
    @patch("api.views.get_classified_tiles_view.Classification")
    @patch("api.views.get_classified_tiles_view.Tile")
    def test_get_classified_tiles_one_classification_classifier(self, mock_tile, mock_classification,
                                                                mock_transformer, mock_tile_to_coordinates):
        """
        @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
        @patch("api.views.get_classified_tiles_view.Transformer")
        @patch("api.views.get_classified_tiles_view.Classification")
        @patch("api.views.get_classified_tiles_view.Tile")
        def test_get_classified_tiles_one_classification_classifier(self, mock_tile, mock_classification,
                                                                    mock_transformer, mock_tile_to_coordinates)
        """

        parameters = {
            "year": 2021,
            "province": "None",
        }
        transformer = 50, 60
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classification = Classification(tile=tile, year=2005, contains_greenery=True,
                                        greenery_percentage=0.165, classified_by=-1)

        mock_query_set_tile = MagicMock(spec=Tile.objects)
        tiles = [tile]
        mock_query_set_tile.filter.return_value = tiles
        mock_tile.objects = mock_query_set_tile
        mock_query_set_classification = MagicMock(spec=Classification.objects)
        mock_query_set_classification.filter.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value.distinct = MagicMock()
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.__len__ = \
            MagicMock(return_value=1)
        classifications = [classification]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values_list = \
            MagicMock(return_value=classifications)
        classifications_dict = [classification.__dict__]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values = \
            MagicMock(return_value=classifications_dict)
        mock_classification.objects = mock_query_set_classification
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {
                "xmin": tile_to_coordinates["xmin"],
                "ymin": tile_to_coordinates["ymin"],
                "xmax": tile_to_coordinates["xmax"],
                "ymax": tile_to_coordinates["ymax"],
                "x_coordinate": transformer[0],
                "y_coordinate": transformer[1],
                "year": 2005,
                "classified_by": "classifier",
                "contains_greenery": True,
                "greenery_amount": "low",
            }
        ])
        mock_tile.objects.filter.assert_called_once_with(tile_id__in=classifications)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with("tile_id")
        mock_classification.objects.filter.return_value.values.return_value.distinct.assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.__len__.\
            assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values_list.\
            assert_called_once_with("tile_id", flat=True)
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values.\
            assert_called_once_with()
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])
        mock_tile_to_coordinates.assert_called_once_with(tile.x_coordinate, tile.y_coordinate)

    @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
    @patch("api.views.get_classified_tiles_view.Transformer")
    @patch("api.views.get_classified_tiles_view.Classification")
    @patch("api.views.get_classified_tiles_view.Tile")
    def test_get_classified_tiles_one_classification_training_data(self, mock_tile, mock_classification,
                                                                   mock_transformer, mock_tile_to_coordinates):
        """
        @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
        @patch("api.views.get_classified_tiles_view.Transformer")
        @patch("api.views.get_classified_tiles_view.Classification")
        @patch("api.views.get_classified_tiles_view.Tile")
        def test_get_classified_tiles_one_classification_training_data(self, mock_tile, mock_classification,
                                                                       mock_transformer, mock_tile_to_coordinates)
        """

        parameters = {
            "year": 2021,
            "province": "None",
        }
        transformer = 50, 60
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classification = Classification(tile=tile, year=1900, contains_greenery=True,
                                        greenery_percentage=0.445, classified_by=-2)

        mock_query_set_tile = MagicMock(spec=Tile.objects)
        tiles = [tile]
        mock_query_set_tile.filter.return_value = tiles
        mock_tile.objects = mock_query_set_tile
        mock_query_set_classification = MagicMock(spec=Classification.objects)
        mock_query_set_classification.filter.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value.distinct = MagicMock()
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.__len__ = \
            MagicMock(return_value=1)
        classifications = [classification]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values_list = \
            MagicMock(return_value=classifications)
        classifications_dict = [classification.__dict__]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values = \
            MagicMock(return_value=classifications_dict)
        mock_classification.objects = mock_query_set_classification
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {
                "xmin": tile_to_coordinates["xmin"],
                "ymin": tile_to_coordinates["ymin"],
                "xmax": tile_to_coordinates["xmax"],
                "ymax": tile_to_coordinates["ymax"],
                "x_coordinate": transformer[0],
                "y_coordinate": transformer[1],
                "year": 1900,
                "classified_by": "training data",
                "contains_greenery": True,
                "greenery_amount": "medium",
            }
        ])
        mock_tile.objects.filter.assert_called_once_with(tile_id__in=classifications)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with("tile_id")
        mock_classification.objects.filter.return_value.values.return_value.distinct.assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.__len__.\
            assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values_list.\
            assert_called_once_with("tile_id", flat=True)
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values.\
            assert_called_once_with()
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])
        mock_tile_to_coordinates.assert_called_once_with(tile.x_coordinate, tile.y_coordinate)

    @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
    @patch("api.views.get_classified_tiles_view.Transformer")
    @patch("api.views.get_classified_tiles_view.Classification")
    @patch("api.views.get_classified_tiles_view.Tile")
    def test_get_classified_tiles_one_classification_user(self, mock_tile, mock_classification,
                                                          mock_transformer, mock_tile_to_coordinates):
        """
        @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
        @patch("api.views.get_classified_tiles_view.Transformer")
        @patch("api.views.get_classified_tiles_view.Classification")
        @patch("api.views.get_classified_tiles_view.Tile")
        def test_get_classified_tiles_one_classification_user(self, mock_tile, mock_classification,
                                                              mock_transformer, mock_tile_to_coordinates)
        """

        parameters = {
            "year": 2021,
            "province": "None",
        }
        transformer = 50, 60
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        tile = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        classification = Classification(tile=tile, year=2021, contains_greenery=True,
                                        greenery_percentage=0.83, classified_by=1)

        mock_query_set_tile = MagicMock(spec=Tile.objects)
        tiles = [tile]
        mock_query_set_tile.filter.return_value = tiles
        mock_tile.objects = mock_query_set_tile
        mock_query_set_classification = MagicMock(spec=Classification.objects)
        mock_query_set_classification.filter.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value.distinct = MagicMock()
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.__len__ = \
            MagicMock(return_value=1)
        classifications = [classification]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values_list = \
            MagicMock(return_value=classifications)
        classifications_dict = [classification.__dict__]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values = \
            MagicMock(return_value=classifications_dict)
        mock_classification.objects = mock_query_set_classification
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {
                "xmin": tile_to_coordinates["xmin"],
                "ymin": tile_to_coordinates["ymin"],
                "xmax": tile_to_coordinates["xmax"],
                "ymax": tile_to_coordinates["ymax"],
                "x_coordinate": transformer[0],
                "y_coordinate": transformer[1],
                "year": 2021,
                "classified_by": "user",
                "contains_greenery": True,
                "greenery_amount": "high",
            }
        ])
        mock_tile.objects.filter.assert_called_once_with(tile_id__in=classifications)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with("tile_id")
        mock_classification.objects.filter.return_value.values.return_value.distinct.assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.__len__.\
            assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values_list.\
            assert_called_once_with("tile_id", flat=True)
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values.\
            assert_called_once_with()
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_called_once_with(tile_to_coordinates["x_coordinate"],
                                                                                 tile_to_coordinates["y_coordinate"])
        mock_tile_to_coordinates.assert_called_once_with(tile.x_coordinate, tile.y_coordinate)

    @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
    @patch("api.views.get_classified_tiles_view.Transformer")
    @patch("api.views.get_classified_tiles_view.Classification")
    @patch("api.views.get_classified_tiles_view.Tile")
    def test_get_classified_tiles_one_classification_many_classifications(self,
                                                                          mock_tile,
                                                                          mock_classification,
                                                                          mock_transformer,
                                                                          mock_tile_to_coordinates):
        """
        @patch("api.views.get_classified_tiles_view.transform_tile_to_coordinates")
        @patch("api.views.get_classified_tiles_view.Transformer")
        @patch("api.views.get_classified_tiles_view.Classification")
        @patch("api.views.get_classified_tiles_view.Tile")
        def test_get_classified_tiles_one_classification_many_classifications(self,
                                                                              mock_tile,
                                                                              mock_classification,
                                                                              mock_transformer,
                                                                              mock_tile_to_coordinates)
        """

        parameters = {
            "year": 2021,
            "province": "None",
        }
        transformer = 50, 60
        tile_to_coordinates = {
            "xmin": 100,
            "ymin": 200,
            "xmax": 110,
            "ymax": 220,
            "x_coordinate": 105,
            "y_coordinate": 210,
        }
        tile_1 = Tile(tile_id=100, x_coordinate=200, y_coordinate=300)
        tile_2 = Tile(tile_id=400, x_coordinate=500, y_coordinate=600)
        classification_1 = Classification(tile=tile_1, year=2021, contains_greenery=True,
                                          greenery_percentage=0.83, classified_by=1)
        classification_2 = Classification(tile=tile_1, year=2000, contains_greenery=False,
                                          greenery_percentage=0, classified_by=-1)
        classification_3 = Classification(tile=tile_2, year=1950, contains_greenery=True,
                                          greenery_percentage=-1, classified_by=0)
        classification_4 = Classification(tile=tile_2, year=1975, contains_greenery=False,
                                          greenery_percentage=0, classified_by=-2)

        mock_query_set_tile = MagicMock(spec=Tile.objects)
        tiles = [tile_1, tile_2]
        mock_query_set_tile.filter.return_value = tiles
        mock_tile.objects = mock_query_set_tile
        mock_query_set_classification = MagicMock(spec=Classification.objects)
        mock_query_set_classification.filter.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value = mock_query_set_classification
        mock_query_set_classification.filter.return_value.values.return_value.distinct = MagicMock()
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.__len__ = \
            MagicMock(return_value=1)
        classifications = [classification_1, classification_2, classification_3, classification_4]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values_list = \
            MagicMock(return_value=classifications)
        classifications_dict = [classification_1.__dict__, classification_2.__dict__,
                                classification_3.__dict__, classification_4.__dict__]
        mock_query_set_classification.filter.return_value.values.return_value.distinct.return_value.values = \
            MagicMock(return_value=classifications_dict)
        mock_classification.objects = mock_query_set_classification
        mock_transformer.from_crs.return_value = MagicMock()
        mock_transformer.from_crs.return_value.transform = MagicMock(return_value=transformer)
        mock_tile_to_coordinates.return_value = tile_to_coordinates

        request = self.request_factory.get("/urban_development/get_classified_tiles/")
        response = GetClassifiedTilesView.as_view()(request, json.dumps(parameters))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {
                "xmin": tile_to_coordinates["xmin"],
                "ymin": tile_to_coordinates["ymin"],
                "xmax": tile_to_coordinates["xmax"],
                "ymax": tile_to_coordinates["ymax"],
                "x_coordinate": transformer[0],
                "y_coordinate": transformer[1],
                "year": 2021,
                "classified_by": "user",
                "contains_greenery": True,
                "greenery_amount": "high",
            },
            {
                "xmin": tile_to_coordinates["xmin"],
                "ymin": tile_to_coordinates["ymin"],
                "xmax": tile_to_coordinates["xmax"],
                "ymax": tile_to_coordinates["ymax"],
                "x_coordinate": transformer[0],
                "y_coordinate": transformer[1],
                "year": 1975,
                "classified_by": "training data",
                "contains_greenery": False,
                "greenery_amount": "none",
            }
        ])
        mock_tile.objects.filter.assert_called_once_with(tile_id__in=classifications)
        mock_classification.objects.filter.assert_called_once_with(year__lte=parameters["year"])
        mock_classification.objects.filter.return_value.values.assert_called_once_with("tile_id")
        mock_classification.objects.filter.return_value.values.return_value.distinct.assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.__len__.\
            assert_called_once_with()
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values_list.\
            assert_called_once_with("tile_id", flat=True)
        mock_classification.objects.filter.return_value.values.return_value.distinct.return_value.values.\
            assert_called_once_with()
        mock_transformer.from_crs.assert_called_once_with("EPSG:28992", "EPSG:4326")
        mock_transformer.from_crs.return_value.transform.assert_has_calls([call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"]),
                                                                           call(tile_to_coordinates["x_coordinate"],
                                                                                tile_to_coordinates["y_coordinate"])])
        mock_tile_to_coordinates.assert_has_calls([call(tile_1.x_coordinate, tile_1.y_coordinate),
                                                   call(tile_2.x_coordinate, tile_2.y_coordinate)])
