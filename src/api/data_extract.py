from math import floor
from .models import Tile
from pyproj.transformer import TransformerGroup

import pandas


def extract_convert_to_esri():
    tg = TransformerGroup("epsg:4326", "epsg:28992")
    col_list = ['item', 'geo', 'inception']

    # Change here the name of the input file
    df = pandas.read_csv("./data_extraction/query.csv", names=col_list)
    points = df.geo.tolist()
    years = df.inception.tolist()

    points.pop(0)
    years.pop(0)

    # Change the year of the map
    year_map = 2010

    # Change here the name of the output file
    f = open("./data_extraction/parks_tiles.txt", "a")

    for location, year in zip(points, years):
        before_flip = location.split("(")[1][:-1]
        x = before_flip.split(" ")[1]
        y = before_flip.split(" ")[0]
        inception_year = year.split("-")[0]

        x_esri = tg.transformers[0].transform(x, y)[0]
        y_esri = tg.transformers[0].transform(x, y)[1]

        x_esri -= 13328.546
        x_esri /= 406.40102300613496932515337423313

        y_esri = 619342.658 - y_esri
        y_esri /= 406.40607802340702210663198959688

        x_esri = floor(x_esri) + 75120
        y_esri = floor(y_esri) + 75032

        url_result = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" \
                     + str(year_map) + "/MapServer/tile/11/" + str(y_esri) + "/" + str(x_esri)

        if inception_year is None:
            inception_year = 2020

        tile = Tile(url=url_result, label="park", year=inception_year)

        tile.save()

        f.write(url_result + " " + inception_year + "\n")

    f.close()


if __name__ == '__main__':
    extract_convert_to_esri()
