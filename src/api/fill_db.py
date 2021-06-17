"""
fill_db.py
"""

from math import floor, ceil
import pandas
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from pyproj import Transformer
from .models import Tile, Classification, User
from .greenery import calculate_percentage_greenery

def create_tiles():
    """
    def create_tiles()
    """

    data_frame = pandas.read_csv("../src/data/tilenames.csv")
    tilenames = data_frame.tilename.tolist()
    percentage = 0

    for i in enumerate(tilenames):
        if ceil((100 * i) / len(tilenames)) > percentage:
            percentage = ceil((100 * i) / len(tilenames))
            print(str(percentage) + "%")

        tile = tilenames[i]
        x_coordinate = int(tile.split("_")[0])
        y_coordinate = int(tile.split("_")[1][:-4])
        tile_id = x_coordinate * 75879 + y_coordinate
        Tile.objects.create_tile(tile_id=tile_id, x_coordinate=x_coordinate, y_coordinate=y_coordinate)


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
            greenery_percentage = calculate_percentage_greenery(x_esri, y_esri, year, contains_greenery)

            Classification.objects.create(tile=Tile(tile_id, x_esri, y_esri), year=year, classified_by="-2",
                                          contains_greenery=contains_greenery, greenery_percentage=greenery_percentage)
        except ObjectDoesNotExist:
            print(x_esri, y_esri)
        except IntegrityError:
            print(x_esri, y_esri)


def manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery):
    """
    def manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery):
    """
    x_tile, y_tile = transform_coordinates_to_tile(x_coordinate, y_coordinate)

    try:
        Classification.objects.create(tile_id=Tile.objects.
                                      get(x_coordinate=x_tile, y_coordinate=y_tile).tile_id,
                                      year=year, greenery_percentage=greenery_percentage,
                                      contains_greenery=contains_greenery,
                                      classified_by=User.objects.get(email=user).id)

    except IntegrityError:
        Classification.objects.filter(year=year, tile_id=Tile.objects.get(x_coordinate=x_tile,
                                                                          y_coordinate=y_tile).tile_id)\
            .update(greenery_percentage=greenery_percentage, contains_greenery=contains_greenery,
                    classified_by=User.objects.get(email=user).id)

    except ObjectDoesNotExist:
        print("Unsuccessfully updated tiles.")


def transform_coordinates_to_tile(x_coordinate, y_coordinate):
    """
    def transform_coordinates_to_tile(x_coordinate, y_coordinate):
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992")
    x_esri, y_esri = transformer.transform(x_coordinate, y_coordinate)
    x_esri -= 13328.546
    x_esri /= 406.40102300613496932515337423313

    y_esri = 619342.658 - y_esri
    y_esri /= 406.40607802340702210663198959688

    x_tile = floor(x_esri) + 75120
    y_tile = floor(y_esri) + 75032

    return x_tile, y_tile


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
