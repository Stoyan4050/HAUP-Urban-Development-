"""
utils.py
"""
import urllib
from math import floor, ceil
import random
import os
import cv2
import pandas
import requests
import numpy as np
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pyproj import Transformer
from .classifier import color_detection
from .models import Tile, Classification, User
from .tokens import TOKEN_GENERATOR


def add_labels_for_previous_years():
    """
    add_labels_for_previous_years()
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
                            tile=Tile.objects.get(x_coordinate=tile_x, y_coordinate=tile_y), year=year + 10,
                            greenery_percentage=classification.greenery_percentage, classified_by="-2")
                    except ObjectDoesNotExist:
                        print(tile_x, tile_y)
                os.remove("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year) + ".jpg")
                break
            if year == 1900:
                os.remove("./data/images/" + str(tile_x) + "_" + str(tile_y) + "_" + str(year) + ".jpg")
                # print(year)
                Classification.objects.create(
                    tile=Tile.objects.get(x_coordinate=tile_x, y_coordinate=tile_y), year=year,
                    greenery_percentage=classification.greenery_percentage, classified_by="-2")

    # for year in range(1910, 2030, 10):
    #
    #     print(str(year - 10) + ": " + str(np.percentile(arr[int((year - 1910) / 10)], 90)) + "\n")


def add_user_label(start_x, start_y, length_x, length_y, year, label, user_id):
    """
    def add_user_label(start_x, start_y, length_x, length_y, year, label, user_id)
    """

    for x_coordinate in range(start_x, start_x + length_x - 1):
        for y_coordinate in range(start_y, start_y + length_y - 1):

            try:
                Classification.objects.create(
                    tile=Tile.objects.get(x_coordinate=x_coordinate, y_coordinate=y_coordinate),
                    year=year, label=label, classified_by=user_id)
            except ObjectDoesNotExist:
                print(x_coordinate, y_coordinate)


def create_tiles():
    """
    def create_tiles()
    """

    data_frame = pandas.read_csv("../src/data/tilenames.csv")
    tilenames = data_frame.tilename.tolist()
    percentage = 0

    for i in range(0, len(tilenames)):
        if ceil((100 * i) / len(tilenames)) > percentage:
            percentage = ceil((100 * i) / len(tilenames))
            print(str(percentage) + "%")

        tile = tilenames[i]
        x_coordinate = int(tile.split("_")[0])
        y_coordinate = int(tile.split("_")[1][:-4])
        tile_id = x_coordinate * 75879 + y_coordinate
        Tile.objects.create_tile(tile_id=tile_id, x_coordinate=x_coordinate, y_coordinate=y_coordinate)


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


def extract_available_years():
    """
    def extract_available_years()
    """

    page = requests.get("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services")
    soup = BeautifulSoup(page.content, 'html.parser')
    years = {}

    for hyperlink in soup.select("ol[id=serviceList] > li > a[id=l1]"):
        if hyperlink.text.startswith("Historische_tijdreis_"):
            reference = hyperlink.text[len("Historische_tijdreis_"):]

            if "_" in reference:
                for i in range(int(reference[: reference.index("_")]), int(reference[reference.index("_") + 1:]) + 1):
                    years[i] = reference
            else:
                years[int(reference)] = reference

    if 2020 not in years:
        years[2020] = "2020"

    return years


def extract_convert_to_esri():
    """
    def extract_convert_to_esri()
    """

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992")

    # Change here the name of the input file
    data_frame = pandas.read_csv("./data/Wikidata/data.csv")

    points = data_frame.geo.tolist()
    years = [2020 for _ in range(len(data_frame))]
    greenery = data_frame.contains_greenery.tolist()

    if 'inception' in data_frame.columns:
        years = data_frame.inception.tolist()
        count = 0
        percentage = 0
        points_length = len(points)

    for location, year, contains_greenery in zip(points, years, greenery):
        if ceil((100 * count) / points_length) > percentage:
            percentage = ceil((100 * count) / points_length)
            print(str(percentage) + "%")
        count += 1
        before_flip = location.split("(")[1][:-1]
        y_coordinate, x_coordinate = before_flip.split(" ")
        x_esri, y_esri = transformer.transform(x_coordinate, y_coordinate)

        if isinstance(year, str):
            year = int(str(year.split("-")[0]))
        else:
            year = 2020

        x_esri -= 13328.546
        x_esri /= 406.40102300613496932515337423313

        y_esri = 619342.658 - y_esri
        y_esri /= 406.40607802340702210663198959688

        x_esri = floor(x_esri) + 75120
        y_esri = floor(y_esri) + 75032
        tile_id = x_esri * 75879 + y_esri

        first_colored_map = 1914

        try:
            if contains_greenery:
                greenery_percentage = color_detection(x_esri, y_esri, max(year, first_colored_map))
            else:
                greenery_percentage = 0

            Classification.objects.create(tile=Tile(tile_id, x_esri, y_esri), year=year, classified_by="-2",
                                          contains_greenery=contains_greenery, greenery_percentage=greenery_percentage)
        except ObjectDoesNotExist:
            print(x_esri, y_esri)
        except IntegrityError:
            print(x_esri, y_esri)


def send_email(uid, domain, email_subject, email_template):
    """
    def send_email(uid, domain, email_subject, email_template)
    """

    try:
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        user = None

    if user is not None:
        email_message = render_to_string(email_template, {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": TOKEN_GENERATOR.make_token(user),
        })
        email = EmailMessage(email_subject, email_message, to=[user.email])
        email.send()
        return True

    return False


def transform_tile_to_coordinates(x_tile, y_tile):
    """
    def transform_tile_to_coordinates(x_tile, y_tile)
    """

    x_offset = 406.40102300613496932515337423313
    y_offset = 406.40607802340702210663198959688

    xmin = x_tile - 75120
    xmin *= x_offset
    xmin = xmin + 13328.546

    ymax = y_tile - 75032
    ymax *= y_offset
    ymax = 619342.658 - ymax

    xmax = xmin + x_offset
    ymin = ymax - y_offset

    x_coordinate = (xmin + xmax) / 2
    y_coordinate = (ymin + ymax) / 2

    return {
        "xmin": xmin,
        "ymin": ymin,
        "xmax": xmax,
        "ymax": ymax,
        "x_coordinate": x_coordinate,
        "y_coordinate": y_coordinate,
    }
