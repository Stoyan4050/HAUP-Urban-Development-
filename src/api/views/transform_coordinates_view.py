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
            greenery_percentage = "unknown"
            classified_by = "unknown"

        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        x_coordinate, y_coordinate = transformer.transform(x_parameter, y_parameter)

        result = {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
            "classified_by": classified_by,
            "contains_greenery": contains_greenery,
            "greenery_percentage": greenery_percentage,
        }

        return JsonResponse(result, safe=False)
