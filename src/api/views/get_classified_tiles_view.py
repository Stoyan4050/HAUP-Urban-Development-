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

PROVINCES = {"Drenthe": [75590, 75751, 75128, 75290], "Flevoland": [75424, 75574, 75228, 75391],
             "Friesland": [75380, 75641, 75043, 75240], "Gelderland": [75402, 75713, 75316, 75532],
             "Groningen": [75598, 75771, 75032, 75226], "Limburg": [75499, 75613, 75520, 75805],
             "Noord-Brabant": [75264, 75581, 75506, 75672], "Noord-Holland": [75205, 75455, 75133, 75552],
             "Overijssel": [75534, 75750, 75225, 75425], "Zuid-Holland": [75205, 75408, 75368, 75552],
             "Utrecht": [75368, 75509, 75376, 75498], "Zeeland": [75120, 75278, 75526, 75675]}

LOW_MEDIUM_GREENERY = 0.33
MEDIUM_HIGH_GREENERY = 0.66


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
        province = json.loads(parameters).get("province")

        if province == "None":
            classifications_for_year = Classification.objects.filter(year__lte=year).values("tile_id").distinct()
        else:
            x_min = PROVINCES.get(province)[0]
            x_max = PROVINCES.get(province)[1]
            y_min = PROVINCES.get(province)[2]
            y_max = PROVINCES.get(province)[3]

            tiles = Tile.objects.filter(x_coordinate__gte=x_min, x_coordinate__lte=x_max,
                                        y_coordinate__gte=y_min, y_coordinate__lte=y_max)
            classifications_for_year = Classification.objects.filter(year__lte=year, tile_id__in=tiles
                                                                     .values_list("tile_id", flat=True)).distinct()

        if len(classifications_for_year) <= 0:
            return HttpResponseBadRequest("No tiles have been classified for the selected year.")

        distinct_tiles = Tile.objects.filter(tile_id__in=classifications_for_year.values_list("tile_id", flat=True))

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
                "contains_greenery": "unknown",
                "greenery_amount": "unknown",
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

                if classification["contains_greenery"]:
                    if 0 <= classification["greenery_percentage"] <= LOW_MEDIUM_GREENERY:
                        result[classification["tile_id"]]["greenery_amount"] = "low"
                    elif LOW_MEDIUM_GREENERY < classification["greenery_percentage"] <= MEDIUM_HIGH_GREENERY:
                        result[classification["tile_id"]]["greenery_amount"] = "medium"
                    elif MEDIUM_HIGH_GREENERY < classification["greenery_percentage"] <= 1:
                        result[classification["tile_id"]]["greenery_amount"] = "high"
                    else:
                        result[classification["tile_id"]]["greenery_amount"] = "unknown"
                else:
                    result[classification["tile_id"]]["greenery_amount"] = "none"

        return JsonResponse(list(result.values()), safe=False)
