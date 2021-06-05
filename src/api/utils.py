"""
utils.py
"""
import urllib
from math import floor, ceil
import cv2
import random
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
from .models import Tile, Classification, User
from .tokens import TOKEN_GENERATOR


def add_user_label(start_x, start_y, length_x, length_y, year, label, user_id):
    """
    def add_user_label(start_x, start_y, length_x, length_y, year, label, user_id)
    """

    for x_coordinate in range(start_x, start_x + length_x - 1):
        for y_coordinate in range(start_y, start_y + length_y - 1):

            try:
                Classification.objects.create(
                    tile_id=Tile.objects.get(x_coordinate=x_coordinate, y_coordinate=y_coordinate),
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

                urllib.request.urlretrieve(res, str(rand_x) + "_" + str(rand_y) + "_" + str(year) + ".jpg")
                if year != 1900:
                    image = cv2.imread(str(rand_x) + "_" + str(rand_y) + "_" + str(year) + ".jpg")
                    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    histogram1 = cv2.calcHist([gray_image1], [0],
                                              None, [256], [0, 256])

                    image = cv2.imread(str(rand_x) + "_" + str(rand_y) + "_" + str(year - 10) + ".jpg")
                    gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    histogram2 = cv2.calcHist([gray_image2], [0],
                                              None, [256], [0, 256])
                    distance = 0

                    # Euclidean Distace
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

    np.percentile(arr[0], 90)
    print(count)

    a_file = open("test.txt", "w")
    for year in range(1910, 2030, 10):
        a_file.write(str(year) + ": " + str(np.percentile(arr[int((year - 1910) / 10)], 90)) + "\n")

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
    contain_greenery = data_frame.contains_greenery.tolist()
    years = [2020 for _ in range(len(data_frame))]

    if 'inception' in data_frame.columns:
        years = data_frame.inception.tolist()
        count = 0
        percentage = 0
        points_length = len(points)

    for location, year, contains_greenery in zip(points, years, contain_greenery):

        if ceil((100 * count) / points_length) > percentage:
            percentage = ceil((100 * count) / points_length)
            print(str(percentage) + "%")
        count += 1
        before_flip = location.split("(")[1][:-1]
        y_coordinate, x_coordinate = before_flip.split(" ")
        x_esri, y_esri = transformer.transform(x_coordinate, y_coordinate)

        if isinstance(year, str):
            year = str(year.split("-")[0])
        else:
            year = 2020

        x_esri -= 13328.546
        x_esri /= 406.40102300613496932515337423313

        y_esri = 619342.658 - y_esri
        y_esri /= 406.40607802340702210663198959688

        x_esri = floor(x_esri) + 75120
        y_esri = floor(y_esri) + 75032
        tile_id = x_esri * 75879 + y_esri

        # try:
        #     Classification.objects.create(tile_id=tile_id, year=year,
        #                                   contains_greenery=contains_greenery, classified_by="-2")
        # except ObjectDoesNotExist:
        #     print(x_esri, y_esri)

        try:
            Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=x_esri, y_coordinate=y_esri), year=year,
                                          contains_greenery=contains_greenery, classified_by="-2")
        except ObjectDoesNotExist:
            print(x_esri, y_esri)
        except IntegrityError:
            if contains_greenery:
                classification = Classification.objects.get(tile_id=tile_id, year=year)
                classification.contains_greenery = True
                classification.save()
                # Classification.objects.replace(tile_id=Tile.objects.get(x_coordinate=x_esri, y_coordinate=y_esri),
                #                                year=year, contains_greenery=contains_greenery, classified_by="-2")


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
