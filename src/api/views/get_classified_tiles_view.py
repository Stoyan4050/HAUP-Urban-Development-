"""
get_classified_tiles_view.py
"""

import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View
from pyproj import Transformer
from api.models.classification import Classification
from api.models.tile import Tile
from api.utils.transform_tile_to_coordinates import transform_tile_to_coordinates
from api.utils.calculate_greenery_rounded import calculate_greenery_rounded


class GetClassifiedTilesView(View):
    """
    class GetClassifiedTilesView(View)
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters)
        """

        year = json.loads(parameters).get("year")

        classifications_for_year = Classification.objects.filter(year__lte=year)

        if len(classifications_for_year) <= 0:
            return HttpResponseBadRequest("No tiles have been classified for the selected year.")

        distinct_ids = classifications_for_year.values("tile_id").distinct()
        distinct_tiles = Tile.objects.filter(tile_id__in=distinct_ids.values_list("tile_id", flat=True))
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        result = {}

        for tile in distinct_tiles:
            coordinates = transform_tile_to_coordinates(tile.x_coordinate, tile.y_coordinate)
            x_coordinate, y_coordinate = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])

            result[tile.tile_id] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": x_coordinate,
                "y_coordinate": y_coordinate,
                "year": -1,
                "classified_by": "unknown",
                "contains_greenery": False,
                "greenery_percentage": 0,
                "greenery_rounded": 0,
            }

        for classification in classifications_for_year.values():
            if result[classification["tile_id"]]["year"] < classification["year"]:
                result[classification["tile_id"]]["year"] = classification["year"]

                if classification["classified_by"] == -1:
                    result[classification["tile_id"]]["classified_by"] = "classifier"
                elif classification["classified_by"] <= -2:
                    result[classification["tile_id"]]["classified_by"] = "training data"
                elif classification["classified_by"] > 0:
                    result[classification["tile_id"]]["classified_by"] = "user"
                else:
                    result[classification["tile_id"]]["classified_by"] = "unknown"

                result[classification["tile_id"]]["contains_greenery"] = classification["contains_greenery"]
                result[classification["tile_id"]]["greenery_percentage"] = 100 * classification["greenery_percentage"]
                result[classification["tile_id"]]["greenery_rounded"] = calculate_greenery_rounded(
                    classification["contains_greenery"], classification["greenery_percentage"])

        return JsonResponse(list(result.values()), safe=False)
