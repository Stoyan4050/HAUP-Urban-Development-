"""
extract_convert_to_esri.py
"""

from math import floor, ceil
import pandas
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from pyproj import Transformer
from api.models.classification import Classification
from api.models.tile import Tile
from api.utils.calculate_greenery_percentage import calculate_greenery_percentage


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

        try:
            greenery_percentage = calculate_greenery_percentage(x_esri, y_esri, year, contains_greenery)

            Classification.objects.create(tile=Tile(tile_id, x_esri, y_esri), year=year, classified_by="-2",
                                          contains_greenery=contains_greenery, greenery_percentage=greenery_percentage)
        except ObjectDoesNotExist:
            print(x_esri, y_esri)
        except IntegrityError:
            print(x_esri, y_esri)
