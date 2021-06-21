"""
manual_classification_view.py
"""

import json
from django.http import JsonResponse
from django.views import View
from api.utils.calculate_greenery_rounded import calculate_greenery_rounded
from api.utils.manual_classify import manual_classify
from api.utils.transform_coordinates_to_tile import transform_coordinates_to_tile
from api.utils.transform_tile_to_coordinates import transform_tile_to_coordinates


class ManualClassificationView(View):
    """
    class ManualClassificationView(View):
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters):
        """

        x_coordinate = json.loads(parameters).get("latitude")
        y_coordinate = json.loads(parameters).get("longitude")
        year = json.loads(parameters).get("year")
        user = json.loads(parameters).get("classified_by")
        greenery_percentage = json.loads(parameters).get("greenery_percentage")
        contains_greenery = json.loads(parameters).get("contains_greenery")

        if user != "guest":
            manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery)

        contains_greenery = contains_greenery.lower()

        if contains_greenery in ("true", "false"):
            greenery_rounded = calculate_greenery_rounded(contains_greenery == "true", greenery_percentage)
        else:
            greenery_rounded = 0

        x_tile, y_tile = transform_coordinates_to_tile(x_coordinate, y_coordinate)
        coordinates = transform_tile_to_coordinates(x_tile, y_tile)

        result = {
            "xmin": coordinates["xmin"],
            "ymin": coordinates["ymin"],
            "xmax": coordinates["xmax"],
            "ymax": coordinates["ymax"],
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
            "contains_greenery": contains_greenery,
            "greenery_percentage": greenery_percentage,
            "greenery_rounded": greenery_rounded,
        }

        return JsonResponse(result, safe=False)
