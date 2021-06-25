"""
manual_classification_view.py
"""

import json
from django.http import JsonResponse
from django.views import View
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

        user = json.loads(parameters).get("classified_by")

        if user == "guest":
            return JsonResponse(None, safe=False)

        x_coordinate = json.loads(parameters).get("longitude")
        y_coordinate = json.loads(parameters).get("latitude")
        year = json.loads(parameters).get("year")
        contains_greenery = json.loads(parameters).get("contains_greenery")
        greenery_amount = json.loads(parameters).get("greenery_amount")

        if contains_greenery == "True":
            if greenery_amount == "low":
                greenery_percentage = 0.165
            elif greenery_amount == "medium":
                greenery_percentage = 0.445
            else:
                greenery_percentage = 0.83
        else:
            greenery_percentage = 0

        manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery)

        contains_greenery = contains_greenery.lower()

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
            "greenery_amount": greenery_amount,
        }

        return JsonResponse(result, safe=False)
