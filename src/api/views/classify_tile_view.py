"""
classify_tile_view.py
"""

import json
from django.http import JsonResponse
from django.views import View
from pyproj import Transformer
from api.utils.transform_coordinates_to_tile import transform_coordinates_to_tile
from api.utils.transform_tile_to_coordinates import transform_tile_to_coordinates
from classification.classifier_cnn import classify_cnn

LOW_MEDIUM_GREENERY = 0.33
MEDIUM_HIGH_GREENERY = 0.66


class ClassifyTileView(View):
    """
    class ClassifyTileView(View)
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters)
        """

        user = json.loads(parameters).get("user")

        if user == "guest":
            return JsonResponse(None, safe=False)

        year = json.loads(parameters).get("year")
        x_parameter = float(json.loads(parameters).get("longitude"))
        y_parameter = float(json.loads(parameters).get("latitude"))

        x_tile, y_tile = transform_coordinates_to_tile(x_parameter, y_parameter)

        tile_id = x_tile * 75879 + y_tile

        response = classify_cnn(year, tile_id)

        if response is None:
            return JsonResponse(None, safe=False)

        coordinates = transform_tile_to_coordinates(x_tile, y_tile)
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        center_x, center_y = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])

        contains_greenery = response["contains_greenery"]
        greenery_percentage = response["greenery_percentage"]

        if contains_greenery != "unknown":
            if contains_greenery:
                if 0 <= greenery_percentage <= LOW_MEDIUM_GREENERY:
                    greenery_amount = "low"
                elif LOW_MEDIUM_GREENERY < greenery_percentage <= MEDIUM_HIGH_GREENERY:
                    greenery_amount = "medium"
                elif MEDIUM_HIGH_GREENERY < greenery_percentage <= 1:
                    greenery_amount = "high"
                else:
                    greenery_amount = "unknown"
            else:
                greenery_amount = "none"
        else:
            greenery_amount = "unknown"

        result = {
            "xmin": coordinates["xmin"],
            "ymin": coordinates["ymin"],
            "xmax": coordinates["xmax"],
            "ymax": coordinates["ymax"],
            "x_coordinate": center_x,
            "y_coordinate": center_y,
            "contains_greenery": contains_greenery,
            "greenery_amount": greenery_amount,
        }

        return JsonResponse(result, safe=False)
