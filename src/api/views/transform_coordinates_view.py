"""
transform_coordinates_view.py
"""

import json
from math import floor
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from pyproj import Transformer
from api.models.classification import Classification
from api.utils.transform_coordinates_to_tile import transform_coordinates_to_tile
from api.utils.transform_tile_to_coordinates import transform_tile_to_coordinates


class TransformCoordinatesView(View):
    """
    class TransformCoordinatesView(View):
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters):
        """

        year = json.loads(parameters).get("year")
        x_parameter = json.loads(parameters).get("x_coordinate")
        y_parameter = json.loads(parameters).get("y_coordinate")

        x_tile = x_parameter - 13328.546
        x_tile /= 406.40102300613496932515337423313

        y_tile = 619342.658 - y_parameter
        y_tile /= 406.40607802340702210663198959688

        x_tile = floor(x_tile) + 75120
        y_tile = floor(y_tile) + 75032

        tile_id = x_tile * 75879 + y_tile

        try:
            classifications = Classification.objects.filter(tile=tile_id, year__lte=year)

            classification_year = -1
            for classification in classifications.values():
                if classification["year"] > classification_year:
                    classification_year = classification["year"]

            contains_greenery = Classification.objects.get(tile=tile_id, year=classification_year).contains_greenery
            greenery_percentage = Classification.objects.get(tile=tile_id, year=classification_year).greenery_percentage
            classified_by = Classification.objects.get(tile=tile_id, year=classification_year).classified_by

            if classified_by == -1:
                classified_by = "classifier"
            elif classified_by <= -2:
                classified_by = "training data"
            elif classified_by > 0:
                classified_by = "user"
            else:
                classified_by = "unknown"
        except ObjectDoesNotExist:
            contains_greenery = "unknown"
            greenery_amount = "unknown"
            classified_by = "unknown"

        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        x_coordinate, y_coordinate = transformer.transform(x_parameter, y_parameter)

        tile_coordinate_x, tile_coordinate_y = transform_coordinates_to_tile(x_coordinate, y_coordinate)
        coordinates = transform_tile_to_coordinates(tile_coordinate_x, tile_coordinate_y)
        center_x, center_y = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])

        if not contains_greenery == "unknown":
            if contains_greenery:
                if 0 <= greenery_percentage <= 0.33:
                    greenery_amount = "low"
                elif 0.33 < greenery_percentage <= 0.66:
                    greenery_amount = "medium"
                elif 0.66 < greenery_percentage <= 1:
                    greenery_amount = "high"
                else:
                    greenery_amount = "unknown"
            else:
                greenery_amount = "none"

        result = {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "xmin": coordinates["xmin"],
            "ymin": coordinates["ymin"],
            "xmax": coordinates["xmax"],
            "ymax": coordinates["ymax"],
            "x_coordinate": center_x,
            "y_coordinate": center_y,
            "classified_by": classified_by,
            "contains_greenery": contains_greenery,
            "greenery_amount": greenery_amount,
        }

        return JsonResponse(result, safe=False)
