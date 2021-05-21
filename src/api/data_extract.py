import pandas
from .models import Tile, Classification
from math import floor
from pyproj import Transformer

def extract_convert_to_esri():
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992")

    # Change here the name of the input file
    df = pandas.read_csv("./api/data_extraction/data.csv")
    
    points = df.geo.tolist()
    points.pop(0)
    
    labels = df.label.tolist()
    labels.pop(0)
    
    if 'inception' in df.columns:
        years = df.inception.tolist()
        years.pop(0)
    
    # Change here the name of the output file
    # f = open("./api/data_extraction/query_tiles.txt", "a")

    # This part of the code was used to extract all the non-blank tiles and put it in the database.
    # df1 = pandas.read_csv("./api/data_extraction/tilenames.csv")
    # tile_names = df1.filename.tolist()
    # for tile in tile_names:
    #     Tile.objects.create_tile(x_coordinate=tile.split("_")[0], y_coordinate=tile.split("_")[1][:-4])

    for location, year, label in zip(points, years, labels):
        before_flip = location.split("(")[1][:-1]
        x, y = before_flip.split(" ")
        x_esri, y_esri = transformer.transform(x, y)
        
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

    #     url_result = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" \
    #                  + str(year_map) + "/MapServer/tile/11/" + str(y_esri) + "/" + str(x_esri)
        
        try:
            Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=x_esri, y_coordinate=y_esri), year=year,
                                          label=label, classified_by="-2")
        except Tile.DoesNotExist:
            print(x_esri, y_esri)
            continue
