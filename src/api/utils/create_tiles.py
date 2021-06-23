"""
create_tiles.py
"""

from math import ceil
import pandas
from api.models.tile import Tile


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
