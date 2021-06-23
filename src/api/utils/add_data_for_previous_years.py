"""
add_data_for_previous_years.py
"""

import urllib
import os
import cv2
from django.core.exceptions import ObjectDoesNotExist
from api.models.classification import Classification
from api.models.tile import Tile


def add_data_for_previous_years():
    """
    add_data_for_previous_years()
    """

    # arr = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    percentile_dictionary = {

        1900: 7623.754980468751,
        1910: 8686.396484375,
        1920: 9016.2767578125,
        1930: 12544.352734375001,
        1940: 9720.98046875,
        1950: 15607.060644531251,
        1960: 12649.3212890625,
        1970: 12715.7212890625,
        1980: 14023.113671875015,
        1990: 20844.1919921875,
        2000: 25589.086328125006,
        2010: 21873.5953125
    }

    ind = 0
    classifications = Classification.objects.filter(year=2020)

    for classification in classifications:
        ind += 1
        print(ind)

        tile_id = classification.tile.tile_id
        tile_x = classification.tile.tile_id // 75879
        tile_y = int(classification.tile.tile_id) % 75879

        res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + \
              "2020" + "/MapServer/tile/11/" + str(tile_y) + "/" + str(tile_x)
        # print(res)
        urllib.request.urlretrieve(res, "./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + "2020" + ".jpg")

        for year in range(2010, 1890, -10):
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + \
                  str(year) + "/MapServer/tile/11/" + str(tile_y) + "/" + str(tile_x)
            urllib.request.urlretrieve(res, "./data/images/" + str(tile_x) + "_" +
                                       str(tile_y) + "_" + str(year) + ".jpg")

            image = cv2.imread("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year) + ".jpg")
            gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            histogram1 = cv2.calcHist([gray_image1], [0],
                                      None, [256], [0, 256])

            image = cv2.imread("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year + 10) + ".jpg")
            gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            histogram2 = cv2.calcHist([gray_image2], [0],
                                      None, [256], [0, 256])

            os.remove("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year + 10) + ".jpg")

            distance = 0

            # Euclidean Distance
            i = 0
            while i < len(histogram1) and i < len(histogram2):
                distance += (histogram1[i] - histogram2[i]) ** 2
                i += 1
            distance = distance ** (1 / 2)

            # arr[int((year - 1900) / 10)].append(distance)

            # print(year, distance, percentile_dictionary[year], percentile_dictionary[year] - distance)

            if distance > percentile_dictionary[year]:
                # print(year)
                if year != 2010:
                    try:
                        Classification.objects.create(
                            tile=Tile(tile_id, tile_x, tile_y), year=year + 10,
                            greenery_percentage=classification.greenery_percentage, classified_by="-2")
                    except ObjectDoesNotExist:
                        print(tile_x, tile_y)
                os.remove("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year) + ".jpg")
                break

            if year == 1900:
                os.remove("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year) + ".jpg")
                # print(year)
                Classification.objects.create(
                    tile=Tile(tile_id, tile_x, tile_y), year=year,
                    greenery_percentage=classification.greenery_percentage, classified_by="-2")

    # for year in range(1910, 2030, 10):
    #
    #     print(str(year - 10) + ": " + str(np.percentile(arr[int((year - 1910) / 10)], 90)) + "\n")
