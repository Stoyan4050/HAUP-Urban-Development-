"""
euclidean_distance_random_tiles.py
"""

import urllib
import random
import os
import cv2
import numpy as np
from django.core.exceptions import ObjectDoesNotExist
from api.models.tile import Tile


def euclidean_distance_random_tiles():
    """
    def euclidean_distance_random_tiles()
    """

    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    arr = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(1, 500):
        rand_x = random.randint(75087, 75825)
        rand_y = random.randint(74956, 75879)

        try:
            Tile.objects.get(x_coordinate=rand_x, y_coordinate=rand_y)

            for year in range(1900, 2030, 10):
                res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + \
                      str(year) + "/MapServer/tile/11/" + str(rand_y) + "/" + str(rand_x)

                urllib.request.urlretrieve(res, "./data/images/" + str(rand_x) + "_" +
                                           str(rand_y) + "_" + str(year) + ".jpg")
                if year != 1900:
                    image = cv2.imread("./data/images/" + str(rand_x) + "_" + str(rand_y) + "_" + str(year) + ".jpg")
                    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    histogram1 = cv2.calcHist([gray_image1], [0],
                                              None, [256], [0, 256])

                    image = cv2.imread("./data/images/" + str(rand_x) + "_" +
                                       str(rand_y) + "_" + str(year - 10) + ".jpg")
                    gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    histogram2 = cv2.calcHist([gray_image2], [0],
                                              None, [256], [0, 256])

                    os.remove("./data/images/" + str(rand_x) + "_" + str(rand_y) + "_" + str(year - 10) + ".jpg")

                    distance = 0

                    # Euclidean Distance
                    i = 0
                    while i < len(histogram1) and i < len(histogram2):
                        distance += (histogram1[i] - histogram2[i]) ** 2
                        i += 1
                    distance = distance ** (1 / 2)

                    if distance > 1:
                        print(int((year - 1910) / 10))
                        arr[int((year - 1910) / 10)].append(distance)
                        print(distance, rand_y, rand_x)
                        count[int(distance / 10000)] += 1

        except ObjectDoesNotExist:
            pass

    print(count)

    a_file = open("year_percentiles.txt", "w")
    for year in range(1910, 2030, 10):
        a_file.write(str(year - 10) + ": " + str(np.percentile(arr[int((year - 1910) / 10)], 90)) + "\n")

    a_file.close()
