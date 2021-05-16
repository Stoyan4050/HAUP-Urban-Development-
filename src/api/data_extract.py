from math import floor
from .models import Tile, Classification
from pyproj.transformer import TransformerGroup

import pandas


def extract_convert_to_esri():
    tg = TransformerGroup("epsg:4326", "epsg:28992")

    # Change here the name of the input file
    df = pandas.read_csv("./api/data_extraction/data.csv")
    points = df.geo.tolist()
    points.pop(0)
    labels = df.label.tolist()
    labels.pop(0)
    years = []
    if 'inception' in df.columns:
        years = df.inception.tolist()
        years.pop(0)

    # Change the year of the map
    # year_map = 2020

    # Change here the name of the output file
    # f = open("./api/data_extraction/query_tiles.txt", "a")

    # This part of the code was used to extract all the non-blank tiles and put it in the database.
    # df1 = pandas.read_csv("./api/data_extraction/tilenames.csv")
    # tile_names = df1.filename.tolist()
    # for tile in tile_names:
        # Tile.objects.create_tile(x_coordinate=tile.split("_")[0], y_coordinate=tile.split("_")[1][:-4])
    for location, year, label in zip(points, years, labels):
        before_flip = location.split("(")[1][:-1]
        x = before_flip.split(" ")[1]
        y = before_flip.split(" ")[0]
        # inception_year = year.split("-")[0]

        x_esri = tg.transformers[0].transform(x, y)[0]
        y_esri = tg.transformers[0].transform(x, y)[1]
        if year != "Unknown":
            year = str(year.split("-")[0])
        x_esri -= 13328.546
        x_esri /= 406.40102300613496932515337423313

        y_esri = 619342.658 - y_esri
        y_esri /= 406.40607802340702210663198959688

        x_esri = floor(x_esri) + 75120
        y_esri = floor(y_esri) + 75032

    #     url_result = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" \
    #                  + str(year_map) + "/MapServer/tile/11/" + str(y_esri) + "/" + str(x_esri)
        try:
            Tile.objects.get(x_coordinate=x_esri, y_coordinate=y_esri)
            Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=x_esri, y_coordinate=y_esri), year=year,
                                          label=label, classified_by="-2")
        except Tile.DoesNotExist:
            print(x_esri, y_esri)
            continue


        # f.write(url_result + " " + inception_year + "\n")

    # f.close()
