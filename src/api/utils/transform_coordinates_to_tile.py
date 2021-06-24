"""
transform_coordinates_to_tile.py
"""

from math import floor
from pyproj import Transformer


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
